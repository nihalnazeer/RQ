from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from app.database.models import SalesTransaction, ProductMaster
from datetime import datetime, timedelta

class RevenueCalculator:
    
    @staticmethod
    def calculate_total_revenue(db: Session, start_date: datetime, end_date: datetime):
        """Calculate total revenue with metrics"""
        result = db.query(
            func.sum(SalesTransaction.quantity_sold * SalesTransaction.sale_price).label("total_revenue"),
            func.count(SalesTransaction.id).label("total_transactions"),
            func.avg(SalesTransaction.sale_price).label("avg_sale_price")
        ).filter(
            and_(
                SalesTransaction.transaction_date >= start_date,
                SalesTransaction.transaction_date <= end_date
            )
        ).first()
        
        total_revenue = float(result.total_revenue) if result.total_revenue else 0.0
        
        return {
            "total_revenue": total_revenue,
            "total_transactions": result.total_transactions or 0,
            "average_sale_price": float(result.avg_sale_price) if result.avg_sale_price else 0.0,
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": (end_date - start_date).days
            }
        }
    
    @staticmethod
    def get_revenue_by_day(db: Session, days: int = 30):
        """Revenue trend breakdown by day"""
        start_date = datetime.now() - timedelta(days=days)
        
        results = db.query(
            func.date(SalesTransaction.transaction_date).label("date"),
            func.sum(SalesTransaction.quantity_sold * SalesTransaction.sale_price).label("revenue"),
            func.count(SalesTransaction.id).label("transaction_count")
        ).filter(SalesTransaction.transaction_date >= start_date)\
         .group_by(func.date(SalesTransaction.transaction_date))\
         .order_by("date").all()
        
        return [
            {
                "date": str(r.date),
                "revenue": float(r.revenue),
                "transactions": r.transaction_count
            } for r in results
        ]
