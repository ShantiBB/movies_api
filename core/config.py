from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    postgres_name: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str


class DjangoSettings(BaseSettings):
    django_secret_key: str
    django_debug: bool
    django_allowed_hosts: list


class Settings(PostgresSettings, DjangoSettings):

    class Config:
        env_file = '.env'

settings = Settings()
