from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()

# print(f"Database Hostname: {settings.database_hostname}")
# print(f"Database Port: {settings.database_port}")
# print(f"Database Hostname: {settings.database_password}")
# print(f"Database Port: {settings.database_username}")