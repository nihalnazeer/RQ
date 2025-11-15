from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from app.database.models import SalesTransaction, ProductMaster
from datetime import datetime, timedelta

class CategoryRevenueAnalyzer:
    
    @staticmethod
    def calculate_category_revenue(db: Session, start_date: datetime = None, end_date: datetime = None):
        """Revenue breakdown by category"""
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        
        results = db.query(
            ProductMaster.category,
            ProductMaster.sub_category,
            func.sum(SalesTransaction.quantity_sold).label("quantity"),
            func.sum(SalesTransaction.quantity_sold * SalesTransaction.sale_price).label("revenue"),
            func.count(SalesTransaction.id).label("transaction_count")
        ).join(ProductMaster, SalesTransaction.sku_id == ProductMaster.sku_id)\
         .filter(
            and_(
                SalesTransaction.transaction_date >= start_date,
                SalesTransaction.transaction_date <= end_date
            )
        ).group_by(ProductMaster.category, ProductMaster.sub_category)\
         .order_by(func.sum(SalesTransaction.quantity_sold * SalesTransaction.sale_price).desc()).all()
        
        total_revenue = sum(float(r.revenue) if r.revenue else 0 for r in results)
        
        return [
            {
                "category": r.category,
                "sub_category": r.sub_category,
                "quantity_sold": r.quantity or 0,
                "revenue": float(r.revenue) if r.revenue else 0.0,
                "percentage_of_total": round(
                    (float(r.revenue) / total_revenue * 100) if r.revenue and total_revenue > 0 else 0, 2
                ),
                "transaction_count": r.transaction_count or 0
            } for r in results
        ]
