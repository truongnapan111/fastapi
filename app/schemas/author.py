from pydantic import BaseModel

class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    """Schema for creating a new author."""

    pass


class AuthorUpdate(AuthorBase):
    """Schema for updating an existing author."""

    name: str | None = None
    bio: str | None = None


class AuthorInDBBase(AuthorBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic will read the data even if it is not a dict, but an ORM model (like SQLAlchemy model)


class Author(AuthorInDBBase):
    """Schema for returning an author."""

    pass
