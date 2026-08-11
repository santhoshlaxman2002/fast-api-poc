from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str
    # TODO: @property
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

# TODO: @lru_cache -> Need to add a package Need to see the usage
settings = Settings()