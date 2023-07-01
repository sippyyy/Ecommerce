from pydantic import BaseSettings

class Settings(BaseSettings):
    db_name:str
    db_hostname:str
    db_username:str
    db_password:str
    db_port:str
    
    class Config:
        env_file = ".env"
        
settings = Settings()
