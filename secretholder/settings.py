from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB_NAME: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    SSO_SERVER_HOST: str
    SSO_SERVER_PORT: int
    SSO_URL_PATH: str
    SSO_PROTOCOL: str = "http"

    PWD_MANAGER_HOST: str
    PWD_MANAGER_PORT: int

    DEFAULT_POSTGRES_DB_NAME: str = "postgres"

    @property
    def dsn_kwargs(self) -> dict:
        return {
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "database": self.POSTGRES_DB_NAME,
        }

    @property
    def default_dsn_kwargs(self) -> str:
        return {
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "database": self.DEFAULT_POSTGRES_DB_NAME,
        }

    @property
    def sso_handler_url(self) -> str:
        return f"{self.SSO_PROTOCOL}://{self.SSO_SERVER_HOST}:{self.SSO_SERVER_PORT}/{self.SSO_URL_PATH}"

    @property
    def sso_base_url(self) -> str:
        return f"{self.SSO_PROTOCOL}://{self.SSO_SERVER_HOST}:{self.SSO_SERVER_PORT}"


settings = Settings()
