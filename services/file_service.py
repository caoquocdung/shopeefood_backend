import os
import uuid
import shutil
from typing import List, Optional
from fastapi import UploadFile, HTTPException
from pathlib import Path

class FileService:
    def __init__(self):
        # Tạo thư mục lưu ảnh
        self.upload_dir = Path("../assets/food_images")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Các định dạng ảnh được phép
        self.allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        
        # Kích thước file tối đa (5MB)
        self.max_file_size = 5 * 1024 * 1024
        #TODO: nén file khi vượt quá kích thước

    async def save_food_image(self, file: UploadFile, item_id: int) -> str:
        """
        Lưu ảnh food và trả về URL
        """
        try:
            # Kiểm tra định dạng file
            file_extension = Path(file.filename).suffix.lower()
            if file_extension not in self.allowed_extensions:
                raise HTTPException(
                    status_code=400, 
                    detail=f"File type not allowed. Allowed types: {', '.join(self.allowed_extensions)}"
                )

            # Kiểm tra kích thước file
            file_content = await file.read()
            if len(file_content) > self.max_file_size:
                raise HTTPException(
                    status_code=400,
                    detail="File size too large. Maximum size is 5MB"
                )

            # Tạo tên file unique
            unique_filename = f"{item_id}_{uuid.uuid4().hex}{file_extension}"
            file_path = self.upload_dir / unique_filename

            # Lưu file
            with open(file_path, "wb") as buffer:
                buffer.write(file_content)

            # Trả về URL tương đối
            return f"../assets/food_images/{unique_filename}"

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    async def save_multiple_menuItem_images(self, files: List[UploadFile], food_id: int) -> List[str]:
        """
        Lưu nhiều ảnh cho một food
        """
        image_urls = []
        for file in files:
            url = await self.save_food_image(file, food_id)
            image_urls.append(url)
        return image_urls

    def delete_menuItem_image(self, image_url: str) -> bool:
        """
        Xóa ảnh food
        """
        try:
            # Lấy tên file từ URL
            filename = Path(image_url).name
            file_path = self.upload_dir / filename
            
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception:
            return False

    def delete_multiple_food_images(self, image_urls: List[str]) -> int:
        """
        Xóa nhiều ảnh, trả về số ảnh đã xóa thành công
        """
        deleted_count = 0
        for url in image_urls:
            if self.delete_food_image(url):
                deleted_count += 1
        return deleted_count
