from sqlalchemy import select
from cloudinary.uploader import upload, destroy
from cloudinary.exceptions import Error as CloudinaryError
from schemas import Image  # SQLModel schema
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

class ImageService:
    async def upload_image(self, image_file, blog_id: uuid.UUID, db: AsyncSession):
        try:
            upload_result = upload(image_file, folder="blog_images")
            image = Image(
                id=uuid.uuid4(),
                url=upload_result["secure_url"],
                public_id=upload_result["public_id"],
                blog_id=blog_id
            )
            db.add(image)
            await db.commit()
            await db.refresh(image)
            return image
        except CloudinaryError as e:
            print(f"Error uploading image: {e}")
            return None

    async def delete_image(self, image_id: uuid.UUID, db: AsyncSession):
        result = await db.execute(select(Image).where(Image.id == image_id))
        image = result.scalar_one_or_none()

        if not image:
            raise ValueError("Image not found")

        try:
            destroy(image.public_id)
        except CloudinaryError as e:
            print(f"[CloudinaryError] Failed to delete image {image.public_id}: {e}")

        await db.delete(image)
        await db.commit()

    async def get_image(self, image_id: uuid.UUID, db: AsyncSession):
        result = await db.execute(select(Image).where(Image.id == image_id))
        return result.scalar_one_or_none()
