from fastapi import APIRouter

router = APIRouter(prefix="/stock", tags=["Stock"])

@router.get("/")
def stock_status():
    return {"message": "Stock endpoint placeholder"}
