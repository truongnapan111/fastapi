from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    published_year = Column(Integer, nullable=False)
    cover_image = Column(String(255), nullable=True)
    author_id = Column(ForeignKey("authors.id", ondelete="RESTRICT"), nullable=False)
    category_id = Column(ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship with Author and Category
    category = relationship("Category", back_populates="books")
    author = relationship("Author", back_populates="books")