from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from app.database.models import SalesTransaction, ProductMaster, StockReceipt
from datetime import datetime, timedelta

class ProfitCalculator:
    
    @staticmethod
    def calculate_profit_metrics(db: Session, start_date: datetime = None, end_date: datetime = None):
        """Calculate total profit and margin"""
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        
        # Sales data
        sales_result = db.query(
            func.sum(SalesTransaction.quantity_sold * SalesTransaction.sale_price).label("total_revenue"),
            func.sum(SalesTransaction.quantity_sold).label("total_qty_sold")
        ).filter(
            and_(
                SalesTransaction.transaction_date >= start_date,
                SalesTransaction.transaction_date <= end_date
            )
        ).first()
        
        total_revenue = float(sales_result.total_revenue) if sales_result.total_revenue else 0.0
        
        # Cost of goods sold (from sales transactions with product cost)
        cogs_result = db.query(
            func.sum(
                SalesTransaction.quantity_sold * ProductMaster.unit_cost_price
            ).label("total_cogs")
        ).join(ProductMaster, SalesTransaction.sku_id == ProductMaster.sku_id)\
         .filter(
            and_(
                SalesTransaction.transaction_date >= start_date,
                SalesTransaction.transaction_date <= end_date
            )
        ).first()
        
        total_cogs = float(cogs_result.total_cogs) if cogs_result.total_cogs else 0.0
        total_profit = total_revenue - total_cogs
        profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0.0
        
        return {
            "total_revenue": total_revenue,
            "cost_of_goods_sold": total_cogs,
            "total_profit": total_profit,
            "profit_margin_percentage": round(profit_margin, 2),
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
        }
    
    @staticmethod
    def get_profit_by_product(db: Session, limit: int = 10):
        """Top products by profit"""
        results = db.query(
            ProductMaster.sku_id,
            ProductMaster.product_name,
            func.sum(SalesTransaction.quantity_sold).label("qty_sold"),
            func.sum(
                SalesTransaction.quantity_sold * SalesTransaction.sale_price
            ).label("revenue"),
            func.sum(
                SalesTransaction.quantity_sold * ProductMaster.unit_cost_price
            ).label("cogs")
        ).join(ProductMaster, SalesTransaction.sku_id == ProductMaster.sku_id)\
         .group_by(ProductMaster.sku_id, ProductMaster.product_name)\
         .order_by(func.sum(SalesTransaction.quantity_sold).desc())\
         .limit(limit).all()
        
        return [
            {
                "sku_id": r.sku_id,
                "product_name": r.product_name,
                "quantity_sold": r.qty_sold or 0,
                "revenue": float(r.revenue) if r.revenue else 0.0,
                "cogs": float(r.cogs) if r.cogs else 0.0,
                "profit": float(r.revenue - r.cogs) if r.revenue and r.cogs else 0.0
            } for r in results
        ]
