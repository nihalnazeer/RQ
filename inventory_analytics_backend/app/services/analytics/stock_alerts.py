from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database.models import ProductMaster, StockReceipt, SalesTransaction
from config import get_settings

class StockAlertSystem:
    
    @staticmethod
    def get_stockout_alerts(db: Session, min_threshold: int = None):
        """Get products with low or zero stock"""
        if not min_threshold:
            min_threshold = get_settings().MIN_STOCK_LEVEL
        
        inventory_data = db.query(
            ProductMaster.sku_id,
            ProductMaster.product_name,
            ProductMaster.category,
            ProductMaster.unit_cost_price,
            func.coalesce(func.sum(StockReceipt.quantity_received), 0).label("total_received"),
            func.coalesce(func.sum(SalesTransaction.quantity_sold), 0).label("total_sold")
        ).outerjoin(StockReceipt, ProductMaster.sku_id == StockReceipt.sku_id)\
         .outerjoin(SalesTransaction, ProductMaster.sku_id == SalesTransaction.sku_id)\
         .group_by(
            ProductMaster.sku_id,
            ProductMaster.product_name,
            ProductMaster.category,
            ProductMaster.unit_cost_price
        ).all()
        
        alerts = []
        for item in inventory_data:
            current_qty = item.total_received - item.total_sold
            
            if current_qty == 0:
                alerts.append({
                    "sku_id": item.sku_id,
                    "product_name": item.product_name,
                    "category": item.category,
                    "current_quantity": 0,
                    "threshold": min_threshold,
                    "status": "OUT_OF_STOCK",
                    "priority": "CRITICAL"
                })
            elif current_qty < min_threshold:
                alerts.append({
                    "sku_id": item.sku_id,
                    "product_name": item.product_name,
                    "category": item.category,
                    "current_quantity": current_qty,
                    "threshold": min_threshold,
                    "status": "LOW_STOCK",
                    "priority": "HIGH"
                })
        
        return sorted(alerts, key=lambda x: x["priority"], reverse=True)
