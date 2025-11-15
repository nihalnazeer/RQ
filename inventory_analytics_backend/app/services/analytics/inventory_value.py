from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database.models import ProductMaster, StockReceipt, SalesTransaction

class InventoryValueCalculator:
    
    @staticmethod
    def calculate_current_inventory_value(db: Session):
        """Calculate total current inventory value at cost price"""
        
        # Get current inventory quantity per SKU
        inventory_data = db.query(
            ProductMaster.sku_id,
            ProductMaster.product_name,
            ProductMaster.category,
            ProductMaster.unit_cost_price,
            ProductMaster.unit_selling_price,
            func.coalesce(
                func.sum(StockReceipt.quantity_received), 0
            ).label("total_received"),
            func.coalesce(
                func.sum(SalesTransaction.quantity_sold), 0
            ).label("total_sold")
        ).outerjoin(StockReceipt, ProductMaster.sku_id == StockReceipt.sku_id)\
         .outerjoin(SalesTransaction, ProductMaster.sku_id == SalesTransaction.sku_id)\
         .group_by(
            ProductMaster.sku_id,
            ProductMaster.product_name,
            ProductMaster.category,
            ProductMaster.unit_cost_price,
            ProductMaster.unit_selling_price
        ).all()
        
        total_inventory_value = 0.0
        total_quantity = 0
        by_category = {}
        
        for item in inventory_data:
            current_qty = item.total_received - item.total_sold
            
            if current_qty > 0:
                inventory_value = current_qty * item.unit_cost_price
                total_inventory_value += inventory_value
                total_quantity += current_qty
                
                if item.category not in by_category:
                    by_category[item.category] = {
                        "category": item.category,
                        "total_value": 0.0,
                        "total_quantity": 0,
                        "products": []
                    }
                
                by_category[item.category]["total_value"] += inventory_value
                by_category[item.category]["total_quantity"] += current_qty
                by_category[item.category]["products"].append({
                    "sku_id": item.sku_id,
                    "product_name": item.product_name,
                    "quantity": current_qty,
                    "unit_cost": float(item.unit_cost_price),
                    "value": inventory_value
                })
        
        return {
            "total_inventory_value": round(total_inventory_value, 2),
            "total_quantity": total_quantity,
            "by_category": list(by_category.values())
        }
