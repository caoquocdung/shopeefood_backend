from typing import List, Optional
from sqlalchemy.orm import Session
from models.food import Food, FoodImage  # Giả sử bạn có models này
from schemas.food_schemas import FoodCreateRequest, FoodResponse
from services.file_service import FileService
from fastapi import UploadFile

class FoodService:
    def __init__(self):
        self.file_service = FileService()

    async def create_food_with_images(
        self, 
        db: Session, 
        food_data: FoodCreateRequest,
        images: List[UploadFile] = None
    ) -> FoodResponse:
        """
        Tạo food mới với ảnh
        """
        try:
            # 1. Tạo food record trong database
            db_food = Food(
                restaurant_id=food_data.restaurant_id,
                category_id=food_data.category_id,
                name=food_data.name,
                description=food_data.description,
                price=food_data.price
            )
            db.add(db_food)
            db.commit()
            db.refresh(db_food)

            image_urls = []
            
            # 2. Upload và lưu ảnh nếu có
            if images:
                for i, image in enumerate(images):
                    # Upload ảnh
                    image_url = await self.file_service.save_food_image(image, db_food.id)
                    
                    # Lưu thông tin ảnh vào database
                    db_image = FoodImage(
                        food_id=db_food.id,
                        url=image_url,
                        is_primary=(i == 0),  # Ảnh đầu tiên là primary
                        sort_order=i + 1
                    )
                    db.add(db_image)
                    image_urls.append(image_url)

                db.commit()

            # 3. Trả về response
            return FoodResponse(
                id=db_food.id,
                restaurant_id=db_food.restaurant_id,
                category_id=db_food.category_id,
                name=db_food.name,
                description=db_food.description,
                price=db_food.price,
                image_urls=image_urls
            )

        except Exception as e:
            db.rollback()
            # Xóa ảnh đã upload nếu có lỗi
            if image_urls:
                self.file_service.delete_multiple_food_images(image_urls)
            raise e

    def get_food_with_images(self, db: Session, food_id: int) -> Optional[FoodResponse]:
        """
        Lấy food với ảnh
        """
        food = db.query(Food).filter(Food.id == food_id).first()
        if not food:
            return None

        # Lấy ảnh của food
        images = db.query(FoodImage).filter(FoodImage.food_id == food_id).order_by(
            FoodImage.is_primary.desc(), FoodImage.sort_order
        ).all()

        image_urls = [img.url for img in images]

        return FoodResponse(
            id=food.id,
            restaurant_id=food.restaurant_id,
            category_id=food.category_id,
            name=food.name,
            description=food.description,
            price=food.price,
            image_urls=image_urls,
            created_at=food.created_at.isoformat()
        )

    async def update_food_images(
        self, 
        db: Session, 
        food_id: int, 
        new_images: List[UploadFile]
    ) -> List[str]:
        """
        Cập nhật ảnh cho food
        """
        # Xóa ảnh cũ
        old_images = db.query(FoodImage).filter(FoodImage.food_id == food_id).all()
        old_urls = [img.url for img in old_images]
        
        # Xóa file ảnh cũ
        self.file_service.delete_multiple_food_images(old_urls)
        
        # Xóa records trong database
        db.query(FoodImage).filter(FoodImage.food_id == food_id).delete()

        # Upload ảnh mới
        new_urls = []
        for i, image in enumerate(new_images):
            image_url = await self.file_service.save_food_image(image, food_id)
            
            db_image = FoodImage(
                food_id=food_id,
                url=image_url,
                is_primary=(i == 0),
                sort_order=i + 1
            )
            db.add(db_image)
            new_urls.append(image_url)

        db.commit()
        return new_urls
