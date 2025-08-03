import logging
import base64
from dataclasses import replace

from typing import Any, Optional, Self

import ormsgpack
from aiogram.filters.state import StateType
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import (
    BaseStorage,
    DefaultKeyBuilder,
    KeyBuilder,
    StorageKey,
)

from nats.aio.client import Client
from nats.js import JetStreamContext
from nats.js.api import KeyValueConfig
from nats.js.errors import NotFoundError
from nats.js.kv import KeyValue

logger = logging.getLogger(__name__)


class NatsStorage(BaseStorage):
    """
    NATS-based FSM storage for Aiogram.

    Stores FSM states and data in NATS JetStream Key-Value buckets.
    Ensures that keys are safely encoded for NATS KV requirements.
    """

    def __init__(
        self,
        nc: Client,
        js: JetStreamContext,
        key_builder: Optional[KeyBuilder] = None,
        fsm_states_bucket: str = "fsm_states_aiogram",
        fsm_data_bucket: str = "fsm_data_aiogram",
    ) -> None:
        """
        Initialize NATS FSM storage.

        :param nc: NATS client instance.
        :param js: JetStream context.
        :param key_builder: Optional custom KeyBuilder for FSM keys.
        :param fsm_states_bucket: Bucket name for FSM states.
        :param fsm_data_bucket: Bucket name for FSM data.
        """
        if key_builder is None:
            key_builder = DefaultKeyBuilder(separator=".")
        self.nc = nc
        self.js = js
        self.fsm_states_bucket = fsm_states_bucket
        self.fsm_data_bucket = fsm_data_bucket
        self._key_builder = key_builder

    async def create_storage(self) -> Self:
        """
        Create required NATS Key-Value buckets for FSM states and data.

        :return: Self (initialized storage).
        """
        self.kv_states = await self._get_kv_states()
        self.kv_data = await self._get_kv_data()
        return self

    async def _get_kv_states(self) -> KeyValue:
        """
        Create or get the KV bucket for FSM states.

        :return: NATS KeyValue bucket instance.
        """
        return await self.js.create_key_value(
            config=KeyValueConfig(
                bucket=self.fsm_states_bucket, history=5, storage="file"
            )
        )

    async def _get_kv_data(self) -> KeyValue:
        """
        Create or get the KV bucket for FSM data.

        :return: NATS KeyValue bucket instance.
        """
        return await self.js.create_key_value(
            config=KeyValueConfig(
                bucket=self.fsm_data_bucket, history=5, storage="file"
            )
        )

    def _b64_encode(self, value: str) -> str:
        """
        Encode a string to URL-safe Base64.

        :param value: String to encode.
        :return: Encoded string.
        """
        return base64.urlsafe_b64encode(value.encode()).decode()

    def _encode_destiny(self, key: StorageKey) -> StorageKey:
        """
        Encode only the `destiny` field of StorageKey to Base64 for safe KV usage.

        :param key: Original StorageKey.
        :return: New StorageKey with encoded destiny.
        """
        if key.destiny:
            encoded_destiny = self._b64_encode(key.destiny)
            safe_key = replace(key, destiny=encoded_destiny)
            return safe_key
        return key

    def _build_safe_key(self, key: StorageKey) -> str:
        """
        Build a full FSM key and ensure it is safe for NATS KV.

        :param key: StorageKey to process.
        :return: Safe string key for NATS.
        """
        safe_key = self._key_builder.build(self._encode_destiny(key))
        return safe_key

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        """
        Save FSM state for a given key.

        :param key: StorageKey identifying the FSM context.
        :param state: State to save (or None to clear).
        """
        state = state.state if isinstance(state, State) else state
        await self.kv_states.put(
            self._build_safe_key(key), ormsgpack.packb(state or None)
        )

    async def get_state(self, key: StorageKey) -> Optional[str]:
        """
        Retrieve FSM state for a given key.

        :param key: StorageKey identifying the FSM context.
        :return: State string or None if not found.
        """
        try:
            entry = await self.kv_states.get(self._build_safe_key(key))
            data = ormsgpack.unpackb(entry.value)
        except NotFoundError:
            return None
        return data

    async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None:
        """
        Save FSM data dictionary for a given key.

        :param key: StorageKey identifying the FSM context.
        :param data: Dictionary to store.
        """
        await self.kv_data.put(self._build_safe_key(key), ormsgpack.packb(data))

    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        """
        Retrieve FSM data for a given key.

        :param key: StorageKey identifying the FSM context.
        :return: Data dictionary or empty dict if not found.
        """
        try:
            entry = await self.kv_data.get(self._build_safe_key(key))
            return ormsgpack.unpackb(entry.value)
        except NotFoundError:
            return {}

    async def close(self) -> None:
        """
        Close the NATS connection.
        """
        await self.nc.close()
