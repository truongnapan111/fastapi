from pydantic import BaseModel
from app.schemas.author import Author
from app.schemas.category import Category
class BookBase(BaseModel):
    title: str
    description: str | None = None
    published_year: int
    cover_image: str | None = None
    author_id: int
    category_id: int

class BookCreate(BookBase):
    """Schema for creating a new book."""

    pass

class BookUpdate(BookBase):
    """Schema for updating an existing book."""

    title: str | None = None
    description: str | None = None
    published_year: int | None = None
    cover_image: str | None = None
    author_id: int | None = None
    category_id: int | None = None

class BookInDBBase(BookBase):
    id: int
    class Config:
        from_attributes = True  # Pydantic will read the data even if it is not a dict, but an ORM model (like SQLAlchemy model)

class Book(BookInDBBase):
    author: Author
    category: Category
