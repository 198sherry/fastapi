from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str = "localhost"
    database_name: str
    database_username: str = "postgres"
    secret_key: str = "23456"
    algorithm: str
    access_token_expire_minutes: int
    
    class Config:
        env_file = ".env"

settings = Settings()