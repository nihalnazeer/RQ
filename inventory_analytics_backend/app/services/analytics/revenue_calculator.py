from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database.models import SalesTransaction
from datetime import datetime, timedelta

class RevenueCalculator:

    @staticmethod
    def calculate_total_revenue(db: Session, start_date: datetime = None, end_date: datetime = None):
        # If no date range provided → full dataset
        if start_date is None:
            start_date = datetime.min
        if end_date is None:
            end_date = datetime.max

        total_revenue = (
            db.query(func.sum(SalesTransaction.quantity_sold * SalesTransaction.sale_price))
            .filter(
                SalesTransaction.transaction_date >= start_date,
                SalesTransaction.transaction_date <= end_date
            )
            .scalar()
        )

        return {
            "total_revenue": float(total_revenue or 0),
            "start_date": start_date,
            "end_date": end_date
        }
