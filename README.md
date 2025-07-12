# 📝 Blog API with FastAPI, SQLModel & Cloudinary

This is a fully asynchronous RESTful Blog API built with **FastAPI** and **SQLModel**, supporting CRUD operations for blog posts with image uploads via **Cloudinary**.

## 🚀 Features

- Async API using FastAPI + SQLAlchemy 2.0 (async engine)
- Blog post CRUD (Create, Read, Update, Delete)
- Upload images to Cloudinary
- Associate multiple images with blog posts
- Update blog fields selectively
- Delete blog and associated Cloudinary images
- UUID-based primary keys
- Relational handling via SQLModel relationships
- OpenAPI documentation auto-generated

## 🛠️ Tech Stack

- FastAPI
- SQLModel + SQLAlchemy (async)
- PostgreSQL (or any SQL-supported DB)
- Cloudinary (for image hosting)
- Uvicorn (ASGI server)
- Python 3.10+

---

## 📁 Project Structure

```
app/
├── main.py
├── models/
│   └── blog.py
├── schemas/
│   └── blog_schema.py
├── services/
│   ├── blog_service.py
│   └── image_service.py
├── routes/
│   └── blog_routes.py
├── db/
│   └── session.py
├── cloudinary_config.py
└── .env
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/twaheedgj/Blog-API.git
cd Blog-API
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file:

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 5. Run Database Migrations

If using Alembic or SQLModel automigrations, initialize the DB. Otherwise, ensure tables are created manually.

### 6. Run the App

```bash
uvicorn app.main:app --reload
```

---

## 📦 API Endpoints

| Method | Endpoint                | Description            |
|--------|-------------------------|------------------------|
| POST   | `/blog/create`          | Create a blog post     |
| GET    | `/blog/blogs`           | Get all blog posts     |
| GET    | `/blog/{title}`         | Get blog(s) by title   |
| GET    | `/blog/{blog_id}`       | Get blog by ID         |
| PUT    | `/blog/{blog_id}`       | Update blog selectively|
| DELETE | `/blog/{blog_id}`       | Delete blog + images   |

### 🖼️ Uploading Images

- Pass `images: List[UploadFile]` via `multipart/form-data` in `POST` or `PUT`.

---

## 🧪 Testing

Coming soon (recommend pytest + httpx)

---

## 🧹 .gitignore Recommendations

```
.env
__pycache__/
*.pyc
venv/
.idea/
.DS_Store
```

---


## 🙋‍♂️ Author

**Talha Waheed**  
[GitHub](https://github.com/twaheedgj) • [LinkedIn](https://www.linkedin.com/in/talhawgj/)

---

## ⭐️ Show Your Support

Give a ⭐️ if you found this useful!