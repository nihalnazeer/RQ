from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database.models import ProductMaster
from datetime import datetime

class ProductAgeAnalyzer:
    
    @staticmethod
    def calculate_average_product_age(db: Session):
        """Calculate average product age in database"""
        results = db.query(
            ProductMaster.sku_id,
            ProductMaster.product_name,
            ProductMaster.category,
            ProductMaster.created_at
        ).all()
        
        product_ages = []
        for product in results:
            age_days = (datetime.utcnow() - product.created_at).days
            product_ages.append({
                "sku_id": product.sku_id,
                "product_name": product.product_name,
                "category": product.category,
                "created_at": product.created_at.isoformat(),
                "age_days": age_days
            })
        
        avg_age = sum(p["age_days"] for p in product_ages) / len(product_ages) if product_ages else 0
        
        return {
            "total_products": len(product_ages),
            "average_product_age_days": round(avg_age, 2),
            "oldest_product_age_days": max([p["age_days"] for p in product_ages]) if product_ages else 0,
            "newest_product_age_days": min([p["age_days"] for p in product_ages]) if product_ages else 0,
            "products_by_age": sorted(product_ages, key=lambda x: x["age_days"], reverse=True)
        }
