from nats.aio.client import Client as NATS
from nats.js import JetStreamContext


async def connect_to_nats(servers: list[str]) -> tuple[NATS, JetStreamContext]:
    nc = NATS()
    await nc.connect(servers)
    js: JetStreamContext = nc.jetstream()

    return nc, js
