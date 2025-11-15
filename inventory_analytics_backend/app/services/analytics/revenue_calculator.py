from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from app.database.models import SalesTransaction, ProductMaster
from datetime import datetime, timedelta

class RevenueCalculator:
    
    @staticmethod
    def calculate_total_revenue(db: Session, start_date: datetime, end_date: datetime):
        ...
