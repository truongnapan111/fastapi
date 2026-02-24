from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "My FastAPI App"
    debug: bool = True
    database_url: str = "sqlite:///./app.db"
    
settings = Settings()