from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.enpoints import author, books, category
app = FastAPI(
    title="Book Management API",
    description="A simple API for managing books in a library.",
    version="1.0.0",
)

#Include routers
app.include_router(author.router, prefix="/authors", tags=["authors"])
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(category.router, prefix="/categories", tags=["categories"])

@app.get("/") #127.0.0.1:8000/

def read_root():
    return {"message": "Welcome to the Book Management API!"}