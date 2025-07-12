import uuid
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from models import BlogPostCreate, BlogPostRead ,BlogPostUpdate
from services import blogservice
from typing import List, Optional
blog_router = APIRouter(
    prefix="/blog",
    tags=["blog"]
)

@blog_router.post("/create",response_model=BlogPostRead)
async def create_blog(
    title: str = Form(...),
    description: str = Form(...),
    content: str = Form(...),
    images: list[UploadFile] = File(default=[]),
    db: AsyncSession = Depends(get_session)
):
    blog_data = BlogPostCreate(title=title, description=description, content=content, images=[])
    blog= await blogservice.create_blog(blog_data, db, images)
    if not blog:
        raise HTTPException(status_code=400, detail="Failed to create blog post")
    return blog

@blog_router.get("/blogs", response_model=List[BlogPostRead])
async def get_blogs(db: AsyncSession = Depends(get_session)):
    blogs = await blogservice.get_blogs(db)
    return blogs

@blog_router.get("/by-title/{title}", response_model=List[BlogPostRead])
async def get_blog_posts_by_title(title: str, db: AsyncSession = Depends(get_session)):
    blogs = await blogservice.get_blog_by_title(title, db)
    return blogs

@blog_router.get("/by-id/{blog_id}", response_model=BlogPostRead)
async def get_blog_by_id(blog_id: str, db: AsyncSession = Depends(get_session)):
    blog = await blogservice.get_blog_by_id(blog_id, db)
    return blog
@blog_router.put("/{blog_id}", response_model=BlogPostRead)
async def update_blog(
    blog_id: str,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    image_files: List[UploadFile] = File(default=[]),
    db: AsyncSession = Depends(get_session)
):
    blog_data = BlogPostUpdate(
        title=title,
        description=description,
        content=content
    )

    blog = await blogservice.update_blog(
        blog_id=blog_id,
        blog_data=blog_data,
        db=db,
        image_files=image_files
    )
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@blog_router.delete("/{blog_id}")
async def delete_blog(blog_id: str, db: AsyncSession = Depends(get_session)):
    result = await blogservice.delete_blog(blog_id, db)
    return result