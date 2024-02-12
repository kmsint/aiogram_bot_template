from typing import Any, Dict, Optional

import ormsgpack
from aiogram.filters.state import StateType
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage, StorageKey
from nats.aio.client import Client
from nats.js.errors import NotFoundError
from nats.js.kv import KeyValue


class NatsStorage(BaseStorage):
    def __init__(self, nc: Client, kv_states: KeyValue, kv_data: KeyValue):
        super().__init__()
        self.nc = nc
        self.kv_states = kv_states
        self.kv_data = kv_data

    @staticmethod
    def _key_formatter(key: StorageKey) -> str:
        return f"{key.bot_id}:{key.user_id}:{key.chat_id}:{key.destiny}"

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        state = state.state if isinstance(state, State) else state
        await self.kv_states.put(
            self._key_formatter(key), ormsgpack.packb(state or None)
        )

    async def get_state(self, key: StorageKey) -> Optional[str]:
        try:
            entry = await self.kv_states.get(self._key_formatter(key))
            data = ormsgpack.unpackb(entry.value)
        except NotFoundError:
            return None
        return data

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        await self.kv_data.put(self._key_formatter(key), ormsgpack.packb(data))

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        try:
            entry = await self.kv_data.get(self._key_formatter(key))
            return ormsgpack.unpackb(entry.value)
        except NotFoundError:
            return {}

    async def close(self) -> None:
        await self.nc.close()
