from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from database import get_db  # Giả sử bạn có database connection
from services.food_service import FoodService
from schemas.food_schemas import FoodCreateRequest, FoodResponse

router = APIRouter(prefix="/api/foods", tags=["foods"])
food_service = FoodService()

@router.post("/", response_model=FoodResponse)
async def create_food(
    # Nhận data dưới dạng form
    restaurant_id: int = Form(...),
    category_id: int = Form(...),
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    # Nhận nhiều ảnh
    images: List[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Tạo food mới với ảnh
    """
    try:
        # Tạo food data object
        food_data = FoodCreateRequest(
            restaurant_id=restaurant_id,
            category_id=category_id,
            name=name,
            description=description,
            price=price
        )

        # Tạo food với ảnh
        result = await food_service.create_food_with_images(db, food_data, images)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{food_id}", response_model=FoodResponse)
def get_food(food_id: int, db: Session = Depends(get_db)):
    """
    Lấy thông tin food với ảnh
    """
    food = food_service.get_food_with_images(db, food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food

@router.put("/{food_id}/images")
async def update_food_images(
    food_id: int,
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    Cập nhật ảnh cho food
    """
    try:
        new_urls = await food_service.update_food_images(db, food_id, images)
        return {"message": "Images updated successfully", "image_urls": new_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/images/{filename}")
async def get_image(filename: str):
    """
    Serve ảnh static
    """
    file_path = f"assets/food_images/{filename}"
    try:
        return FileResponse(file_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Image not found")

@router.delete("/{food_id}")
def delete_food(food_id: int, db: Session = Depends(get_db)):
    """
    Xóa food và ảnh
    """
    try:
        # Lấy thông tin food
        food = food_service.get_food_with_images(db, food_id)
        if not food:
            raise HTTPException(status_code=404, detail="Food not found")

        # Xóa ảnh files
        food_service.file_service.delete_multiple_food_images(food.image_urls)

        # Xóa records trong database
        db.query(FoodImage).filter(FoodImage.food_id == food_id).delete()
        db.query(Food).filter(Food.id == food_id).delete()
        db.commit()

        return {"message": "Food deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
