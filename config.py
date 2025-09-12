from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pg_user: str
    pg_password: str
    pg_host: str
    pg_port: int
    pg_name: str

    app_debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def get_async_db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.pg_user}:"
            f"{self.pg_password}@{self.pg_host}:"
            f"{self.pg_port}/{self.pg_name}"
        )
    


settings = Settings()