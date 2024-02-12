import nats
from nats.js.api import KeyValueConfig

from app.infrastructure.storage.storage.nats_storage import NatsStorage


async def get_nats_storage(
    servers: list[str], buckets: list[KeyValueConfig]
) -> NatsStorage:
    nc = await nats.connect(servers)
    js = nc.jetstream()

    for bucket in buckets:
        await js.create_key_value(config=bucket)

    kv_states = await js.key_value("fsm_states_aiogram")
    kv_data = await js.key_value("fsm_data_aiogram")

    return NatsStorage(nc, kv_states, kv_data)
