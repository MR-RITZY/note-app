from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_hostname: str
    database_port: str
    database_name: str
    algorithm: str
    secret: str
    access_time: int
    refresh_time: int
    
    
    class Config:
        env_file=".env"
        
settings=Settings()