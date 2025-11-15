from sqlalchemy import func, text
from sqlalchemy.orm import Session
from app.database.models import SalesTransaction, ProductMaster
from datetime import datetime, timedelta

class SalesTrendAnalyzer:
    
    @staticmethod
    def calculate_sales_trend(db: Session, days: int = 30):
        """Calculate daily sales trend"""
        start_date = datetime.now() - timedelta(days=days)
        
        results = db.query(
            func.date(SalesTransaction.transaction_date).label("date"),
            func.sum(SalesTransaction.quantity_sold).label("quantity"),
            func.sum(SalesTransaction.quantity_sold * SalesTransaction.sale_price).label("revenue"),
            func.count(SalesTransaction.id).label("transaction_count")
        ).filter(SalesTransaction.transaction_date >= start_date)\
         .group_by(func.date(SalesTransaction.transaction_date))\
         .order_by("date").all()
        
        trend_data = [
            {
                "date": str(r.date),
                "quantity": r.quantity or 0,
                "revenue": float(r.revenue) if r.revenue else 0.0,
                "transactions": r.transaction_count or 0
            } for r in results
        ]
        
        # Calculate trend metrics
        total_qty = sum(t["quantity"] for t in trend_data)
        total_revenue = sum(t["revenue"] for t in trend_data)
        avg_daily_qty = total_qty / len(trend_data) if trend_data else 0
        avg_daily_revenue = total_revenue / len(trend_data) if trend_data else 0
        
        return {
            "trend_period_days": days,
            "total_quantity": total_qty,
            "total_revenue": round(total_revenue, 2),
            "average_daily_quantity": round(avg_daily_qty, 2),
            "average_daily_revenue": round(avg_daily_revenue, 2),
            "daily_data": trend_data
        }
    
    @staticmethod
    def get_weekly_trend(db: Session, weeks: int = 12):
        """Weekly sales trend"""
        start_date = datetime.now() - timedelta(weeks=weeks)
        
        results = db.query(
            func.date_trunc('week', SalesTransaction.transaction_date).label("week"),
            func.sum(SalesTransaction.quantity_sold).label("quantity"),
            func.sum(SalesTransaction.quantity_sold * SalesTransaction.sale_price).label("revenue")
        ).filter(SalesTransaction.transaction_date >= start_date)\
         .group_by(func.date_trunc('week', SalesTransaction.transaction_date))\
         .order_by("week").all()
        
        return [
            {
                "week": str(r.week),
                "quantity": r.quantity or 0,
                "revenue": float(r.revenue) if r.revenue else 0.0
            } for r in results
        ]
