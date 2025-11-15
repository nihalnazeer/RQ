from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.analytics import (
    revenue_calculator,
    profit_calculator,
    inventory_value,
    sales_trend,
    category_revenue,
    best_worst_performer as performers,
    stock_alerts,
    avg_product_age as product_age,
    inventory_vs_cashflow as cash_flow,
    purchase_price_variance as price_variance,
    credit_health,
    forecasting,
    actionable_recommendations as suggestions
)

from datetime import datetime, timedelta

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/revenue")
async def get_total_revenue(
    db: Session = Depends(get_db),
    start_date: datetime = None,
    end_date: datetime = None
):
    """Feature 1: Total Revenue"""
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()
    
    result = revenue_calculator.calculate_total_revenue(db, start_date, end_date)
    return {"status": "success", "data": result}

@router.get("/profit")
async def get_profit_margin(
    db: Session = Depends(get_db),
    start_date: datetime = None,
    end_date: datetime = None
):
    """Feature 2: Total Profit & Profit Margin"""
    result = profit_calculator.calculate_profit_metrics(db, start_date, end_date)
    return {"status": "success", "data": result}

@router.get("/inventory-value")
async def get_inventory_value(db: Session = Depends(get_db)):
    """Feature 3: Total Current Inventory Value"""
    result = inventory_value.calculate_current_inventory_value(db)
    return {"status": "success", "data": result}

@router.get("/sales-trend")
async def get_sales_trend(
    db: Session = Depends(get_db),
    days: int = 30
):
    """Feature 4: Sales Trend"""
    result = sales_trend.calculate_sales_trend(db, days)
    return {"status": "success", "data": result}

@router.get("/category-revenue")
async def get_category_revenue(
    db: Session = Depends(get_db),
    start_date: datetime = None,
    end_date: datetime = None
):
    """Feature 5: Category-wise Revenue"""
    result = category_revenue.calculate_category_revenue(db, start_date, end_date)
    return {"status": "success", "data": result}

@router.get("/performers")
async def get_performers(
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Feature 6: Best & Worst Performers"""
    best = performers.get_best_performers(db, limit)
    worst = performers.get_worst_performers(db, limit)
    return {
        "status": "success",
        "data": {"best_performers": best, "worst_performers": worst}
    }

@router.get("/stock-alerts")
async def get_stock_alerts(db: Session = Depends(get_db)):
    """Feature 7: Stock Out Alerts"""
    alerts = stock_alerts.get_stockout_alerts(db)
    return {"status": "success", "data": alerts}

@router.get("/product-age")
async def get_product_age(db: Session = Depends(get_db)):
    """Feature 8: Average Product Age"""
    result = product_age.calculate_average_product_age(db)
    return {"status": "success", "data": result}

@router.get("/cash-flow")
async def get_cash_flow_analysis(
    db: Session = Depends(get_db),
    days: int = 30
):
    """Feature 9: Inventory Value vs. Cash Outflow"""
    result = cash_flow.analyze_cash_flow(db, days)
    return {"status": "success", "data": result}

@router.get("/price-variance")
async def get_price_variance(db: Session = Depends(get_db)):
    """Feature 10: Purchase Price Variance"""
    result = price_variance.calculate_price_variance(db)
    return {"status": "success", "data": result}

@router.get("/credit-health")
async def get_credit_health(db: Session = Depends(get_db)):
    """Feature 11: Credit Payables / Credit Health"""
    result = credit_health.analyze_credit_health(db)
    return {"status": "success", "data": result}

@router.get("/forecast")
async def get_forecast(
    db: Session = Depends(get_db),
    days: int = 30,
    sku_id: str = None
):
    """Feature 12: Forecasting"""
    if sku_id:
        result = forecasting.forecast_sku(db, sku_id, days)
    else:
        result = forecasting.forecast_all_products(db, days)
    return {"status": "success", "data": result}

@router.get("/suggestions")
async def get_suggestions(db: Session = Depends(get_db)):
    """Feature 13: Actionable Suggestion System"""
    suggestions_list = suggestions.generate_suggestions(db)
    return {"status": "success", "data": suggestions_list}

@router.get("/dashboard")
async def get_dashboard(db: Session = Depends(get_db)):
    """Unified Dashboard with all key metrics"""
    return {
        "status": "success",
        "data": {
            "revenue": revenue_calculator.calculate_total_revenue(db),
            "profit": profit_calculator.calculate_profit_metrics(db),
            "inventory_value": inventory_value.calculate_current_inventory_value(db),
            "alerts": stock_alerts.get_stockout_alerts(db),
            "suggestions": suggestions.generate_suggestions(db),
        }
    }
