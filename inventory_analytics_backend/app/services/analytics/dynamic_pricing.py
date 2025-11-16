"""
app/services/analytics/dynamic_pricing.py

Robust DynamicPricingEngine:
- Works with multiple price variations per SKU
- Uses log-log regression on aggregated (price, quantity) pairs to estimate elasticity
- Uses weighted-average baseline price and average daily demand as baseline
- Configurable lookback window (default 90 days)
- Clean fallbacks when data is sparse
"""

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.models import ProductMaster, SalesTransaction, StockReceipt

import numpy as np
from datetime import datetime, timedelta


class DynamicPricingEngine:
    DEFAULT_ELASTICITY_FALLBACK = -1.2
    ELASTICITY_MIN = -5.0
    ELASTICITY_MAX = -0.2

    @staticmethod
    def _get_sales_aggregates(
        db: Session, sku_id: str, lookback_days: int
    ):
        """
        Return aggregated historical (price, total_quantity) pairs and
        total_quantity over the window.
        """
        if lookback_days and lookback_days > 0:
            cutoff = datetime.utcnow() - timedelta(days=lookback_days)
            q = db.query(
                SalesTransaction.sale_price.label("price"),
                func.sum(SalesTransaction.quantity_sold).label("qty")
            ).filter(
                SalesTransaction.sku_id == sku_id,
                SalesTransaction.transaction_date >= cutoff
            ).group_by(SalesTransaction.sale_price)
        else:
            # No cutoff — include all history
            q = db.query(
                SalesTransaction.sale_price.label("price"),
                func.sum(SalesTransaction.quantity_sold).label("qty")
            ).filter(
                SalesTransaction.sku_id == sku_id
            ).group_by(SalesTransaction.sale_price)

        pairs = q.all()

        # Also fetch total qty and days in window (for daily avg)
        total_qty_q = db.query(func.coalesce(func.sum(SalesTransaction.quantity_sold), 0))\
            .filter(SalesTransaction.sku_id == sku_id)
        if lookback_days and lookback_days > 0:
            total_qty_q = total_qty_q.filter(SalesTransaction.transaction_date >= cutoff)
            days = lookback_days
        else:
            # compute days between first and last sale if available, else use 1
            first_last = db.query(
                func.min(SalesTransaction.transaction_date),
                func.max(SalesTransaction.transaction_date)
            ).filter(SalesTransaction.sku_id == sku_id).first()
            if first_last and first_last[0] and first_last[1]:
                delta = (first_last[1] - first_last[0]).days
                days = max(delta, 1)
            else:
                days = 1

        total_qty = int(total_qty_q.scalar() or 0)

        return pairs, total_qty, days

    # -------------------------------------------------------------
    # Estimate elasticity using aggregated price-quantity pairs
    # -------------------------------------------------------------
    @staticmethod
    def estimate_elasticity_from_pairs(pairs) -> float:
        """
        pairs: iterable of (price, qty)
        returns elasticity (negative number).
        """
        prices = []
        quantities = []

        for p, q in pairs:
            try:
                p_val = float(p)
                q_val = float(q)
            except Exception:
                continue
            if p_val > 0 and q_val > 0:
                prices.append(p_val)
                quantities.append(q_val)

        # Not enough variation → fallback
        if len(prices) < 2 or len(set(prices)) < 2:
            return DynamicPricingEngine.DEFAULT_ELASTICITY_FALLBACK

        X = np.log(np.array(prices))
        Y = np.log(np.array(quantities))

        try:
            b = np.polyfit(X, Y, 1)[0]  # slope is elasticity
        except Exception:
            return DynamicPricingEngine.DEFAULT_ELASTICITY_FALLBACK

        # Cap into sensible bounds: more negative = more elastic
        b_capped = float(max(min(b, DynamicPricingEngine.ELASTICITY_MAX), DynamicPricingEngine.ELASTICITY_MIN))
        return b_capped

    # -------------------------------------------------------------
    # Predict demand at a candidate price using elasticity
    # -------------------------------------------------------------
    @staticmethod
    def predict_demand(base_price: float, base_daily_qty: float, elasticity: float, new_price: float) -> float:
        """
        Demand(p) = base_daily_qty * (new_price / base_price) ^ elasticity
        base_daily_qty is average daily sales (not single-line quantity)
        """
        try:
            if new_price <= 0 or base_price <= 0 or base_daily_qty <= 0:
                return 0.0
            return float(base_daily_qty * (new_price / base_price) ** elasticity)
        except Exception:
            return 0.0

    # -------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------
    @staticmethod
    def recommend_price(
        db: Session,
        sku_id: str,
        clearance_days: int,
        margin_floor: float,
        lookback_days: int = 90,
        candidate_lower_pct: float = 0.5,
        candidate_upper_pct: float = 1.2,
        candidate_steps: int = 50
    ) -> Dict[str, Any]:
        """
        Recommend a price for SKU to meet a clearance_days target while respecting margin_floor.
        - lookback_days: how much history to use to estimate elasticity and baseline demand.
        - candidate price grid from candidate_lower_pct..candidate_upper_pct of original price.
        """

        # 1) Product metadata
        product = db.query(ProductMaster).filter(ProductMaster.sku_id == sku_id).first()
        if not product:
            return {"error": "SKU not found", "sku_id": sku_id}

        cost_price = float(product.unit_cost_price or 0.0)
        original_price = float(product.unit_selling_price or 0.0)

        # 2) Current stock (sum of receipts - sum of sales across all time)
        received = db.query(func.coalesce(func.sum(StockReceipt.quantity_received), 0))\
                    .filter(StockReceipt.sku_id == sku_id).scalar() or 0
        sold = db.query(func.coalesce(func.sum(SalesTransaction.quantity_sold), 0))\
                 .filter(SalesTransaction.sku_id == sku_id).scalar() or 0
        current_stock = int(max(received - sold, 0))

        if current_stock <= 0:
            return {
                "sku_id": sku_id,
                "status": "no_stock",
                "message": "No stock available for pricing"
            }

        # 3) Historical aggregates (price buckets) and baseline daily demand
        pairs, total_qty, days_in_window = DynamicPricingEngine._get_sales_aggregates(db, sku_id, lookback_days)

        # baseline price: weighted average price across pairs (price * qty / total_qty)
        base_price = original_price
        if pairs and total_qty > 0:
            try:
                weighted_sum = sum((float(p) * float(q)) for p, q in pairs if float(p) > 0)
                base_price = float(weighted_sum / total_qty) if total_qty > 0 else original_price
            except Exception:
                base_price = original_price

        # baseline daily quantity: total_qty / days_in_window
        base_daily_qty = float(total_qty) / max(int(days_in_window), 1)

        # If there are no aggregated pairs (no sales), fallback to last sale row if available
        if (not pairs or len(pairs) == 0) and total_qty == 0:
            # try a single last sale row
            last_sale = db.query(SalesTransaction).filter(SalesTransaction.sku_id == sku_id).order_by(SalesTransaction.transaction_date.desc()).first()
            if last_sale:
                base_price = float(last_sale.sale_price or original_price)
                base_daily_qty = float(last_sale.quantity_sold or 1)
            else:
                # No sales history at all: recommend a conservative price = original or cost+margin floor
                fallback_price = max(original_price, cost_price * (1 + margin_floor))
                return {
                    "sku_id": sku_id,
                    "product_name": product.product_name,
                    "category": product.category,
                    "current_price": original_price,
                    "recommended_price": round(fallback_price, 2),
                    "discount_percentage": round(max(0, (original_price - fallback_price) / (original_price or 1) * 100), 2),
                    "cost_price": cost_price,
                    "margin_after_discount": round(fallback_price - cost_price, 2),
                    "margin_floor_used": margin_floor,
                    "current_inventory": current_stock,
                    "clearance_days_target": clearance_days,
                    "projected_daily_sales": 0.0,
                    "projected_days_to_clear": float("inf"),
                    "elasticity_estimate": None,
                    "status": "no_sales_history"
                }

        # 4) Elasticity estimation using aggregated pairs
        elasticity = DynamicPricingEngine.estimate_elasticity_from_pairs(pairs)

        # 5) Required daily sales to clear inventory
        daily_sales_required = float(current_stock) / max(int(clearance_days), 1)

        # 6) Candidate price grid
        if original_price <= 0:
            # if original_price is invalid, fallback to base_price
            price_center = base_price or cost_price * (1 + margin_floor)
        else:
            price_center = original_price

        candidate_prices = np.linspace(
            price_center * candidate_lower_pct,
            price_center * candidate_upper_pct,
            candidate_steps
        )

        best = {
            "price": None,
            "margin": -999999,
            "projected_daily": 0.0,
            "days_to_clear": None
        }

        for p in candidate_prices:
            # enforce margin floor
            min_allowed_price = cost_price * (1 + margin_floor)
            if p < min_allowed_price:
                continue

            projected_daily = DynamicPricingEngine.predict_demand(base_price, base_daily_qty, elasticity, p)

            if projected_daily <= 0:
                continue

            days_to_clear = float(current_stock) / projected_daily if projected_daily > 0 else float("inf")
            margin = p - cost_price

            # Prefer prices that meet clearance time, then maximize margin
            meets_target = days_to_clear <= clearance_days

            if meets_target:
                # if meets target, choose highest margin among those
                if margin > best["margin"] or (best["price"] is None):
                    best.update({
                        "price": p,
                        "margin": margin,
                        "projected_daily": projected_daily,
                        "days_to_clear": days_to_clear
                    })
            else:
                # if nothing meets target yet, keep best (closest days_to_clear but prefer higher margin)
                # we'll consider these only if we don't find any that meet target
                if best["price"] is None:
                    # pick the candidate with the best margin among those (fallback)
                    if margin > best["margin"]:
                        best.update({
                            "price": p,
                            "margin": margin,
                            "projected_daily": projected_daily,
                            "days_to_clear": days_to_clear
                        })

        # 7) Final fallback if nothing picked
        if best["price"] is None:
            # choose at least cost+margin_floor
            fallback_price = max(cost_price * (1 + margin_floor), price_center * 0.9)
            projected_daily = DynamicPricingEngine.predict_demand(base_price, base_daily_qty, elasticity, fallback_price)
            best.update({
                "price": fallback_price,
                "margin": fallback_price - cost_price,
                "projected_daily": projected_daily,
                "days_to_clear": float(current_stock) / projected_daily if projected_daily > 0 else float("inf")
            })

        # 8) Prepare output
        recommended_price = round(float(best["price"]), 2)
        discount_pct = round(max(0.0, (original_price - recommended_price) / (original_price or 1) * 100.0), 2)
        projected_daily_sales = round(float(best["projected_daily"]), 2)
        projected_days_to_clear = round(float(best["days_to_clear"]) if best["days_to_clear"] is not None else float("inf"), 2)

        return {
            "sku_id": sku_id,
            "product_name": product.product_name,
            "category": product.category,
            "current_price": round(original_price, 2),
            "recommended_price": recommended_price,
            "discount_percentage": discount_pct,
            "cost_price": round(cost_price, 2),
            "margin_after_discount": round(recommended_price - cost_price, 2),
            "margin_floor_used": margin_floor,
            "current_inventory": current_stock,
            "clearance_days_target": clearance_days,
            "projected_daily_sales": projected_daily_sales,
            "projected_days_to_clear": projected_days_to_clear,
            "elasticity_estimate": round(elasticity, 4) if elasticity is not None else None,
            "base_price_used": round(base_price, 2),
            "base_daily_qty": round(base_daily_qty, 2),
            "status": "success"
        }
