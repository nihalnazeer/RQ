from fastapi import APIRouter

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.get("/")
def list_sales():
    return {"message": "Sales endpoint placeholder"}
