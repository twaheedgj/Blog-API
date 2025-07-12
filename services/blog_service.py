from fastapi import HTTPException
from schemas import BlogPost
from models import BlogPostCreate, BlogPostRead, BlogPostUpdate
from sqlmodel import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime
from .image_service import ImageService

class BlogService:
    def __init__(self):
        self.image_service = ImageService()

    async def create_blog(self, blog_data: BlogPostCreate, db: AsyncSession, image_files: list):
        blog = BlogPost(
            id=uuid.uuid4(),
            title=blog_data.title,
            description=blog_data.description,
            content="",  # temp empty
            created_at=datetime.now()
        )
        db.add(blog)
        await db.commit()
        await db.refresh(blog)
        placeholder_to_url = {}
        for i, image_file in enumerate(image_files):
            image = await self.image_service.upload_image(image_file.file, blog.id, db)
            placeholder = f"{{{{image{i+1}}}}}"  # e.g., {{image1}}, {{image2}}, etc.
            placeholder_to_url[placeholder] = image.url

        content = blog_data.content
        for placeholder, url in placeholder_to_url.items():
            content = content.replace(placeholder, f"![Image]({url})")

        
        blog.content = content
        await db.commit()
        await db.refresh(blog)

        # Step 5: Return blog with images loaded
        result = await db.execute(
            select(BlogPost).options(selectinload(BlogPost.images)).where(BlogPost.id == blog.id)
        )
        blog_with_images = result.scalar_one()

        return blog_with_images


    async def get_blogs(self, db: AsyncSession):
        result = await db.execute(
            select(BlogPost)
            .options(selectinload(BlogPost.images))
        )
        blogs = result.scalars().all()
        if not blogs:
            return []
        return blogs
    async def get_blog_by_id(self, blog_id: str, db: AsyncSession):
        try:
            blog_uuid = uuid.UUID(blog_id)  # Validate format
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid UUID format")

        result = await db.execute(
            select(BlogPost)
            .options(selectinload(BlogPost.images))  # ensure eager loading works in async
            .where(BlogPost.id == blog_uuid)
        )

        blog = result.scalar_one_or_none()

        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        print(f"Blog found: {blog.title} with ID: {blog.id}")
        return blog
    async def get_blog_by_title(self, title: str, db: AsyncSession):
        result = await db.execute(
            select(BlogPost)
            .options(selectinload(BlogPost.images))
            .where(BlogPost.title.ilike(f"%{title}%"))
        )
        blogs = result.scalars().all()
        if not blogs:
            raise HTTPException(status_code=404, detail=f"No blog posts found with that title: {title}")
        return blogs
    async def update_blog(self, blog_id: str, blog_data: dict, db: AsyncSession, image_files: list = None):
        try:
            blog_uuid = uuid.UUID(blog_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid UUID format")

        result = await db.execute(
            select(BlogPost)
            .where(BlogPost.id == blog_uuid)
            .options(selectinload(BlogPost.images))
        )
        blog = result.scalar_one_or_none()

        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        if blog_data.get("title") is not None:
            blog.title = blog_data["title"]
        if blog_data.get("description") is not None:
            blog.description = blog_data["description"]

        content = blog_data.get("content", blog.content)

        if image_files:
            image_urls = []
            for idx, image_file in enumerate(image_files, start=1):
                image = await self.image_service.upload_image(image_file.file, blog.id, db)
                placeholder = f"{{{{image{idx}}}}}"
                image_markdown = f"![Image]({image.url})"
                content = content.replace(placeholder, image_markdown)
            blog.content = content
        elif content:
            blog.content = content

        await db.commit()
        await db.refresh(blog)
        return blog
    async def delete_blog(self, blog_id: str, db: AsyncSession):
        try:
            blog_uuid = uuid.UUID(blog_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid UUID format")

        result = await db.execute(
            select(BlogPost).where(BlogPost.id == blog_uuid).options(selectinload(BlogPost.images))
        )
        blog = result.scalar_one_or_none()

        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        # Delete associated images
        for image in blog.images:
            await self.image_service.delete_image(image.id, db)

        await db.delete(blog)
        await db.commit()
        return {"detail": "Blog and associated images deleted successfully"}
