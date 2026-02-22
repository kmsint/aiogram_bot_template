from app.config.models import (
    AppConfig,
    BotConfig,
    CacheConfig,
    I18nConfig,
    LogsConfig,
    NatsConfig,
    PostgresConfig,
    RedisConfig,
)
from app.config.settings import settings

_settings = settings


def get_config() -> AppConfig:
    """
    Returns a typed application configuration.

    Returns:
        AppConfig: A validated Pydantic model containing the application settings.
    """
    logs = LogsConfig(
        level_name=_settings.logs.level_name,
        format=_settings.logs.format,
    )

    i18n = I18nConfig(
        default_locale=_settings.i18n.default_locale,
        locales=_settings.i18n.locales,
        locales_map=_settings.i18n.locales_map,
    )

    bot = BotConfig(
        token=_settings.bot_token,
        parse_mode=_settings.bot.parse_mode,
    )

    postgres = PostgresConfig(
        name=_settings.postgres.name,
        host=_settings.postgres.host,
        port=_settings.postgres.port,
        user=_settings.postgres.user,
        password=_settings.postgres_password,
    )

    redis = RedisConfig(
        host=_settings.redis.host,
        port=_settings.redis.port,
        database=_settings.redis.database,
        username=_settings.redis_username,
        password=_settings.redis_password,
    )

    nats = NatsConfig(
        servers=_settings.nats.servers,
        delayed_consumer_subject=_settings.nats.delayed_consumer_subject,
        delayed_consumer_stream=_settings.nats.delayed_consumer_stream,
        delayed_consumer_durable_name=_settings.nats.delayed_consumer_durable_name,
    )

    cache = CacheConfig(use_cache=_settings.cache.use_cache)

    return AppConfig(
        logs=logs,
        i18n=i18n,
        bot=bot,
        postgres=postgres,
        redis=redis,
        nats=nats,
        cache=cache,
    )
