from typing import Any, Mapping, TypeVar, Iterable, Iterator

T = TypeVar("T")


class SingleQueryResult:
    def __init__(self, result: Mapping[str, Any] | None) -> None:
        self._data: dict[str, Any] = dict(result) if result is not None else {}

    @property
    def data(self) -> dict[str, Any]:
        return self._data

    def convert(self, model: type[T]) -> T | None:
        return model(**self._data) if self._data else None

    def __bool__(self) -> bool:
        return bool(self._data)

    def __repr__(self) -> str:
        return f"<SingleQueryResult {self._data}>"


class MultipleQueryResult:
    def __init__(self, results: Iterable[dict[str, Any]] | None = None) -> None:
        self._data: list[dict[str, Any]] = list(results) if results is not None else []

    @property
    def data(self) -> list[dict[str, Any]]:
        return self._data

    def convert_all(self, model: type[T]) -> list[T]:
        return [model(**row) for row in self._data]

    def first(self) -> SingleQueryResult:
        return SingleQueryResult(self._data[0]) if self._data else SingleQueryResult(None)

    def __iter__(self) -> Iterator[dict[str, Any]]:
        return iter(self._data)

    def __getitem__(self, idx: int) -> dict[str, Any]:
        return self._data[idx]

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __repr__(self) -> str:
        return f"<MultipleQueryResult {len(self._data)} rows>"
