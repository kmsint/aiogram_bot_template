import nats
from nats.aio.client import Client
from nats.js import JetStreamContext


async def connect_to_nats(servers: list[str]) -> tuple[Client, JetStreamContext]:
    nc: Client = await nats.connect(servers)
    js: JetStreamContext = nc.jetstream()

    return nc, js
