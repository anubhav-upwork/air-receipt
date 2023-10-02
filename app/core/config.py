import pathlib
from typing import List

from pydantic import AnyHttpUrl, EmailStr
from pydantic_settings import BaseSettings

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    JWT_SECRET: str = "a$$nubh@v_airalpha+$%%receipt+17JulvyTwo1000&23"
    JWT_REFRESH_SECRET_KEY: str = "charlie$%^&&saved_+the-d8123#anubhav#"
    ALGORITHM: str = "HS256"
    UPLOAD_PATH: pathlib.Path = pathlib.Path.joinpath(ROOT, "public/documents")
    ALLOWED_CONTENT: List = ['image/jpeg', 'image/png', 'image/bmp', 'image/tiff', 'application/pdf']
    MAX_FILE_SIZE_KB: int = 5 * 1024

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10  # 10 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # @field_validator("BACKEND_CORS_ORIGINS", pre=True)
    # def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
    #     if isinstance(v, str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, (list, str)):
    #         return v
    #     raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: str = "mysql://anubhav:anubhav123@localhost:3307/air"
    FIRST_SUPERUSER: EmailStr = "admin@recipeapi.com"
    FIRST_SUPERUSER_PW: str = "anubhav.rohatgi"

    # Kafka variables
    class Kafka:
        KAFKA_TOPIC: str = 'docu_push_todo'
        KAFKA_BOOTSTRAP_SERVERS: str = 'localhost:9092'


    class Config:
        case_sensitive = True


settings = Settings()
