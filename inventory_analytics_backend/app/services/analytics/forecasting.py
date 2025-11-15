from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from app.database.models import SalesTransaction, ProductMaster
from datetime import datetime, timedelta
import statistics

class ForecastingEngine:
    
    @staticmethod
    def forecast_sku(db: Session, sku_id: str, forecast_days: int = 30):
        """Simple moving average forecast for a SKU"""
        # Get last 60 days of sales data
        start_date = datetime.now() - timedelta(days=60)
        
        sales_history = db.query(
            func.date(SalesTransaction.transaction_date).label("date"),
            func.sum(SalesTransaction.quantity_sold).label("quantity")
        ).filter(
            and_(
                SalesTransaction.sku_id == sku_id,
                SalesTransaction.transaction_date >= start_date
            )
        ).group_by(func.date(SalesTransaction.transaction_date))\
         .order_by("date").all()
        
        quantities = [r.quantity or 0 for r in sales_history]
        
        if not quantities:
            return {
                "sku_id": sku_id,
                "forecast_available": False,
                "reason": "Insufficient sales history"
            }
        
        # Calculate moving average
        window = 7
        moving_avg = statistics.mean(quantities[-window:]) if len(quantities) >= window else statistics.mean(quantities)
        
        forecast = []
        for day in range(1, forecast_days + 1):
            forecast_date = datetime.now() + timedelta(days=day)
            forecast.append({
                "date": forecast_date.date().isoformat(),
                "forecast_quantity": round(moving_avg)
            })
        
        return {
            "sku_id": sku_id,
            "forecast_days": forecast_days,
            "average_daily_sales": round(moving_avg, 2),
            "forecast": forecast
        }
    
    @staticmethod
    def forecast_all_products(db: Session, forecast_days: int = 30):
        """Forecast for all products"""
        products = db.query(ProductMaster.sku_id).all()
        
        forecasts = []
        for product in products:
            forecast = ForecastingEngine.forecast_sku(db, product.sku_id, forecast_days)
            if forecast.get("forecast_available", True):
                forecasts.append(forecast)
        
        return forecasts
