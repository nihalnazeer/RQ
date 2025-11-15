from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from app.database.models import ProductMaster, SalesTransaction, StockReceipt
from datetime import datetime, timedelta

class SuggestionEngine:
    
    @staticmethod
    def generate_suggestions(db: Session):
        """Generate actionable suggestions"""
        suggestions = []
        
        # 1. Reorder suggestions
        low_stock = SuggestionEngine._get_reorder_suggestions(db)
        suggestions.extend(low_stock)
        
        # 2. Discontinuation suggestions
        slow_movers = SuggestionEngine._get_discontinuation_suggestions(db)
        suggestions.extend(slow_movers)
        
        # 3. Price adjustment suggestions
        high_margin = SuggestionEngine._get_price_adjustment_suggestions(db)
        suggestions.extend(high_margin)
        
        return sorted(suggestions, key=lambda x: x["priority"], reverse=True)
    
    @staticmethod
    def _get_reorder_suggestions(db: Session):
        """Products that need reordering"""
        suggestions = []
        
        inventory_data = db.query(
            ProductMaster.sku_id,
            ProductMaster.product_name,
            func.coalesce(func.sum(StockReceipt.quantity_received), 0).label("total_received"),
            func.coalesce(func.sum(SalesTransaction.quantity_sold), 0).label("total_sold")
        ).outerjoin(StockReceipt, ProductMaster.sku_id == StockReceipt.sku_id)\
         .outerjoin(SalesTransaction, ProductMaster.sku_id == SalesTransaction.sku_id)\
         .group_by(ProductMaster.sku_id, ProductMaster.product_name).all()
        
        for item in inventory_data:
            current_qty = item.total_received - item.total_sold
            if current_qty < 10:
                suggestions.append({
                    "suggestion_type": "REORDER",
                    "sku_id": item.sku_id,
                    "product_name": item.product_name,
                    "reason": f"Current stock: {current_qty} units",
                    "priority": "HIGH" if current_qty == 0 else "MEDIUM",
                    "recommended_action": f"Place reorder for 50 units of {item.product_name}"
                })
        
        return suggestions
    
    @staticmethod
    def _get_discontinuation_suggestions(db: Session):
        """Products with low sales that should be discontinued"""
        suggestions = []
        
        # Products with zero sales in last 90 days
        start_date = datetime.now() - timedelta(days=90)
        
        all_products = db.query(ProductMaster.sku_id, ProductMaster.product_name).all()
        
        for product in all_products:
            sales = db.query(func.sum(SalesTransaction.quantity_sold)).filter(
                and_(
                    SalesTransaction.sku_id == product.sku_id,
                    SalesTransaction.transaction_date >= start_date
                )
            ).first()
            
            if not sales or sales == 0:
                suggestions.append({
                    "suggestion_type": "DISCONTINUE",
                    "sku_id": product.sku_id,
                    "product_name": product.product_name,
                    "reason": "No sales in last 90 days",
                    "priority": "LOW",
                    "recommended_action": f"Consider discontinuing {product.product_name}"
                })
        
        return suggestions
    
    @staticmethod
    def _get_price_adjustment_suggestions(db: Session):
        """Products that may benefit from price adjustments"""
        return []  # Can be extended with ML/pricing logic
