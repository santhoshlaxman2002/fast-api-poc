from fastapi import APIRouter, status, HTTPException, Depends
from app.schemas.product import Product
from app.services.product_service import get_product_service

router = APIRouter()

@router.get("/")
def list_products():
    return []

@router.get("/{product_id}")
def get_product(product_id:int, product_service= Depends(get_product_service)):
    if product_id<=0:
        raise HTTPException(
            status_code=400,
            detail="Invalid product id"
        )
    return product_service.get_product(product_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    return product