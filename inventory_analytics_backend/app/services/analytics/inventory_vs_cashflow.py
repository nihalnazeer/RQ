from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from app.database.models import ProductMaster, StockReceipt, SalesTransaction
from datetime import datetime, timedelta

class CashFlowAnalyzer:
    
    @staticmethod
    def analyze_cash_flow(db: Session, days: int = 30):
        """Analyze cash flow: inventory value vs cash outflow (purchases)"""
        start_date = datetime.now() - timedelta(days=days)
        
        # Total purchases (cash outflow)
        purchases = db.query(
            func.sum(StockReceipt.quantity_received * StockReceipt.unit_cost).label("total_cash_outflow")
        ).filter(StockReceipt.receipt_date >= start_date).first()
        
        total_cash_outflow = float(purchases.total_cash_outflow) if purchases.total_cash_outflow else 0.0
        
        # Total sales (cash inflow)
        sales = db.query(
            func.sum(SalesTransaction.quantity_sold * SalesTransaction.sale_price).label("total_cash_inflow")
        ).filter(SalesTransaction.transaction_date >= start_date).first()
        
        total_cash_inflow = float(sales.total_cash_inflow) if sales.total_cash_inflow else 0.0
        
        # Current inventory value
        inventory_val = db.query(
            func.sum(
                (func.coalesce(func.sum(StockReceipt.quantity_received), 0) - 
                 func.coalesce(func.sum(SalesTransaction.quantity_sold), 0)) * 
                ProductMaster.unit_cost_price
            ).label("inventory_value")
        ).outerjoin(StockReceipt, ProductMaster.sku_id == StockReceipt.sku_id)\
         .outerjoin(SalesTransaction, ProductMaster.sku_id == SalesTransaction.sku_id)\
         .group_by(ProductMaster.sku_id).first()
        
        current_inventory_value = float(inventory_val.inventory_value) if inventory_val.inventory_value else 0.0
        
        net_cash_flow = total_cash_inflow - total_cash_outflow
        
        return {
            "period_days": days,
            "total_cash_inflow": round(total_cash_inflow, 2),
            "total_cash_outflow": round(total_cash_outflow, 2),
            "net_cash_flow": round(net_cash_flow, 2),
            "current_inventory_value": round(current_inventory_value, 2),
            "cash_conversion_ratio": round(
                (total_cash_inflow / total_cash_outflow) if total_cash_outflow > 0 else 0, 2
            )
        }
