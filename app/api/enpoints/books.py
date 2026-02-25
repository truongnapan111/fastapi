from fastapi import APIRouter, Depends, Query, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app import models
from app.schemas.book import Book, BookCreate, BookUpdate

router = APIRouter()


@router.get("/", response_model=List[Book])
def list_books(
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = Query(None),
    category_id: int | None = Query(None),
    keyword: str | None = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Book)
    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)
    if category_id is not None:
        query = query.filter(models.Book.category_id == category_id)
    if keyword is not None and keyword.strip():
        query = query.filter(models.Book.title.contains(keyword.strip()))
    books = query.offset(skip).limit(limit).all()
    return books


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return book


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Check if the referenced author exists
    author = db.query(models.Author).filter(models.Author.id == book.author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Author not found"
        )

    # Check if the referenced category exists
    category = (
        db.query(models.Category).filter(models.Category.id == book.category_id).first()
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found"
        )

    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    # Check if the referenced author exists
    author = db.query(models.Author).filter(models.Author.id == book.author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Author not found"
        )

    # Check if the referenced category exists
    category = (
        db.query(models.Category).filter(models.Category.id == book.category_id).first()
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found"
        )

    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book
