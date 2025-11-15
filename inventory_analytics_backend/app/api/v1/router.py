from fastapi import APIRouter
from app.api.v1.endpoints import products, sales, stock, suppliers, analytics

router = APIRouter()

router.include_router(products.router)
router.include_router(sales.router)
router.include_router(stock.router)
router.include_router(suppliers.router)
router.include_router(analytics.router)
