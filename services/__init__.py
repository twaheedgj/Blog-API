from .user_service import user_service
from .blog_service import BlogService
userservice= user_service()
blogservice = BlogService()
__all__ = ["userservice","blogservice"]