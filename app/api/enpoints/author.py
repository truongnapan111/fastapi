from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app import models
from app.schemas.author import Author, AuthorCreate, AuthorUpdate

router = APIRouter()


@router.get("/", response_model=List[Author])
def list_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = db.query(models.Author).offset(skip).limit(limit).all()
    return authors


@router.get("/{author_id}", response_model=Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )
    return author


@router.post("/", response_model=Author, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    author_exists = (
        db.query(models.Author).filter(models.Author.name == author.name).first()
    )
    if author_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Author already exists"
        )
    if not author.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author name cannot be empty",
        )
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@router.put("/{author_id}", response_model=Author)
def update_author(author_id: int, author: AuthorUpdate, db: Session = Depends(get_db)):
    existing = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )
    if not author.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author name cannot be empty",
        )
    if author.name:
        name_conflict = (
            db.query(models.Author)
            .filter(models.Author.name == author.name, models.Author.id != author_id)
            .first()
        )
        if name_conflict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another author with this name already exists",
            )
    for var, value in vars(author).items():
        if value is not None:
            setattr(existing, var, value)
    db.add(existing)
    db.commit()
    db.refresh(existing)
    return existing


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    existing = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )
    db.delete(existing)
    db.commit()
