from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database.models import SalesTransaction, ProductMaster

class PerformanceAnalyzer:
    
    @staticmethod
    def get_best_performers(db: Session, metric: str = "revenue", limit: int = 10):
        """Get best performing products"""
        query = db.query(
            ProductMaster.sku_id,
            ProductMaster.product_name,
            ProductMaster.category,
            func.sum(SalesTransaction.quantity_sold).label("quantity"),
            func.sum(SalesTransaction.quantity_sold * SalesTransaction.sale_price).label("revenue"),
            func.avg(SalesTransaction.sale_price).label("avg_price")
        ).join(ProductMaster, SalesTransaction.sku_id == ProductMaster.sku_id)\
         .group_by(ProductMaster.sku_id, ProductMaster.product_name, ProductMaster.category)
        
        if metric == "revenue":
            query = query.order_by(func.sum(SalesTransaction.quantity_sold * SalesTransaction.sale_price).desc())
        else:
            query = query.order_by(func.sum(SalesTransaction.quantity_sold).desc())
        
        results = query.limit(limit).all()
        
        return [
            {
                "sku_id": r.sku_id,
                "product_name": r.product_name,
                "category": r.category,
                "quantity_sold": r.quantity or 0,
                "revenue": float(r.revenue) if r.revenue else 0.0,
                "average_price": float(r.avg_price) if r.avg_price else 0.0
            } for r in results
        ]
    
    @staticmethod
    def get_worst_performers(db: Session, limit: int = 10):
        """Get worst performing products"""
        results = db.query(
            ProductMaster.sku_id,
            ProductMaster.product_name,
            func.coalesce(func.sum(SalesTransaction.quantity_sold), 0).label("quantity")
        ).outerjoin(SalesTransaction, ProductMaster.sku_id == SalesTransaction.sku_id)\
         .group_by(ProductMaster.sku_id, ProductMaster.product_name)\
         .order_by(func.coalesce(func.sum(SalesTransaction.quantity_sold), 0).asc())\
         .limit(limit).all()
        
        return [
            {
                "sku_id": r.sku_id,
                "product_name": r.product_name,
                "quantity_sold": r.quantity
            } for r in results
        ]
