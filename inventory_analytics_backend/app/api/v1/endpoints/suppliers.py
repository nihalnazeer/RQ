from fastapi import APIRouter

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.get("/")
def list_suppliers():
    return {"message": "Suppliers endpoint placeholder"}
