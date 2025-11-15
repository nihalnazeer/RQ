from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database.models import ProductMaster, StockReceipt

class PriceVarianceAnalyzer:
    
    @staticmethod
    def calculate_price_variance(db: Session):
        """Analyze variance in purchase prices over time"""
        results = db.query(
            ProductMaster.sku_id,
            ProductMaster.product_name,
            ProductMaster.unit_cost_price,
            func.min(StockReceipt.unit_cost).label("min_cost"),
            func.max(StockReceipt.unit_cost).label("max_cost"),
            func.avg(StockReceipt.unit_cost).label("avg_cost"),
            func.stddev(StockReceipt.unit_cost).label("std_dev"),
            func.count(StockReceipt.id).label("receipt_count")
        ).join(StockReceipt, ProductMaster.sku_id == StockReceipt.sku_id)\
         .group_by(ProductMaster.sku_id, ProductMaster.product_name, ProductMaster.unit_cost_price)\
         .having(func.count(StockReceipt.id) > 1).all()
        
        variance_data = []
        for item in results:
            avg_cost = float(item.avg_cost) if item.avg_cost else 0.0
            price_variance = (
                (float(item.max_cost) - float(item.min_cost)) / avg_cost * 100
                if avg_cost > 0 else 0.0
            )
            
            variance_data.append({
                "sku_id": item.sku_id,
                "product_name": item.product_name,
                "current_cost": float(item.unit_cost_price),
                "minimum_cost": float(item.min_cost),
                "maximum_cost": float(item.max_cost),
                "average_cost": avg_cost,
                "variance_percentage": round(price_variance, 2),
                "receipt_count": item.receipt_count
            })
        
        return sorted(variance_data, key=lambda x: x["variance_percentage"], reverse=True)
