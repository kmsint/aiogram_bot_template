from aiogram.enums import ParseMode
from pydantic import BaseModel, Field


class LogsConfig(BaseModel):
    level_name: str = Field(
        default="INFO", description="Log level name (e.g. DEBUG, INFO, WARNING, ERROR)."
    )
    format: str = Field(
        default="%(asctime)s [%(levelname)s] %(message)s",
        description="Log message format."
    )


class I18nConfig(BaseModel):
    default_locale: str = Field(default="en", description="Default locale for the application.")
    locales: list[str] = Field(default=["en"], description="List of supported locales.")
    locales_map: dict[str, list[str]] = Field(
        ...,
        description="Mapping of base locales to their fallback locales (e.g. {'en': ['en', 'ru']})."
    )


class BotConfig(BaseModel):
    token: str = Field(..., description="Telegram bot API token.")
    parse_mode: ParseMode = Field(
        ..., description="Default parse mode for sending messages (e.g. HTML, Markdown)."
    )


class PostgresConfig(BaseModel):
    name: str = Field(..., description="PostgreSQL database name.")
    host: str = Field(..., description="PostgreSQL server hostname.")
    port: int = Field(..., description="PostgreSQL server port.")
    user: str = Field(..., description="PostgreSQL username.")
    password: str = Field(..., description="PostgreSQL user password.")


class RedisConfig(BaseModel):
    host: str = Field(default="localhost", description="Redis server hostname.")
    port: int = Field(default=6379, description="Redis server port.")
    database: int = Field(default=0, description="Redis database index.")
    username: str | None = Field(None, description="Optional Redis username.")
    password: str | None = Field(None, description="Optional Redis password.")


class NatsConfig(BaseModel):
    servers: str | list[str] = Field(..., description="NATS servers.")
    delayed_consumer_subject: str = Field(..., description="NATS subject for delayed consumer.")
    delayed_consumer_stream: str = Field(..., description="NATS stream for delayed messages.")
    delayed_consumer_durable_name: str = Field(
        ..., description="Durable consumer name for delayed processing."
    )


class CacheConfig(BaseModel):
    use_cache: bool = Field(..., description="Enable or disable in-memory cache usage.")


class AppConfig(BaseModel):
    logs: LogsConfig
    i18n: I18nConfig
    bot: BotConfig
    postgres: PostgresConfig
    redis: RedisConfig
    nats: NatsConfig
    cache: CacheConfig