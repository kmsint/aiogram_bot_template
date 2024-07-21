from dataclasses import dataclass

from environs import Env


@dataclass
class TgBotConfig:
    token: str
    admin_ids: list[int]
    admins_chat: int


@dataclass
class NatsConfig:
    servers: list[str]


@dataclass
class NatsDelayedConsumerConfig:
    subject: str
    stream: str
    durable_name: str


@dataclass
class PostgresConfig:
    db_name: str
    host: str
    port: int
    username: str
    password: str


@dataclass
class RedisConfig:
    use_cache: bool
    database: int
    host: str
    port: int
    username: str
    password: str
    state_ttl: int
    data_ttl: int


@dataclass
class Config:
    tg_bot: TgBotConfig
    nats: NatsConfig
    delayed_consumer: NatsDelayedConsumerConfig
    pg: PostgresConfig
    redis: RedisConfig


def load_config() -> Config:
    env = Env()

    return Config(
        tg_bot=TgBotConfig(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
            admins_chat=env.int('ADMINS_CHAT')
        ),
        nats=NatsConfig(servers=env.list('NATS_SERVERS')),
        delayed_consumer=NatsDelayedConsumerConfig(
            subject=env('NATS_DELAYED_CONSUMER_SUBJECT'),
            stream=env('NATS_DELAYED_CONSUMER_STREAM'),
            durable_name=env('NATS_DELAYED_CONSUMER_DURABLE_NAME')
        ),
        pg=PostgresConfig(
            db_name=env('POSTGRES_NAME'),
            host=env('POSTGRES_HOST'),
            port=env('POSTGRES_PORT'),
            username=env('POSTGRES_USER'),
            password=env('POSTGRES_PASSWORD')
        ),
        redis=RedisConfig(
            use_cache=env.bool('USE_CACHE', False),
            database=env.int('REDIS_DATABASE'),
            host=env('REDIS_HOST'),
            port=env.int('REDIS_PORT'),
            username=env('REDIS_USERNAME'),
            password=env('REDIS_PASSWORD'),
            state_ttl=env('REDIS_TTL_STATE'),
            data_ttl=env('REDIS_TTL_DATA')
        )
    )