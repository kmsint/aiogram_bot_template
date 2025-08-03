from typing import Any, Callable, Mapping, TypeVar, Iterable, Iterator

T = TypeVar("T")


class SingleQueryResult:
    """
    Represents a single-row SQL query result.
    Provides utilities to check emptiness, access raw data,
    and convert the row into a model instance.
    """

    def __init__(self, result: Mapping[str, Any] | None) -> None:
        self._data: dict[str, Any] = dict(result) if result else {}

    @property
    def data(self) -> dict[str, Any]:
        """
        Returns the raw data as a dictionary.
        """
        return self._data

    def is_empty(self) -> bool:
        """
        Returns True if the result is empty (no data).
        """
        return not self._data

    def to_model(
        self, model: Callable[..., T], *, raise_if_empty: bool = False
    ) -> T | None:
        """
        Converts the result to a model instance.

        Args:
            model: A callable model class (e.g., Pydantic, dataclass).
            raise_if_empty: If True, raises ValueError when data is empty.

        Returns:
            An instance of the model or None if empty and raise_if_empty is False.
        """
        if self.is_empty():
            if raise_if_empty:
                raise ValueError("Cannot convert empty result to model")
            return None
        return model(**self._data)

    def as_dict(self) -> dict[str, Any]:
        """
        Returns the result as a plain dictionary (possibly empty).
        """
        return self._data

    def __bool__(self) -> bool:
        return bool(self._data)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, SingleQueryResult) and self._data == other._data

    def __repr__(self) -> str:
        return f"<SingleQueryResult {self._data}>"


class MultipleQueryResult:
    """
    Represents a multi-row SQL query result.
    Provides access to raw rows, transformation to models,
    and helper methods like filtering, sorting, and selection.
    """

    def __init__(self, results: Iterable[Mapping[str, Any]] | None = None) -> None:
        self._data: list[dict[str, Any]] = (
            [dict(row) for row in results] if results else []
        )

    @property
    def data(self) -> list[dict[str, Any]]:
        """
        Returns the raw result rows as a list of dictionaries.
        """
        return self._data

    def is_empty(self) -> bool:
        """
        Returns True if there are no rows in the result.
        """
        return not self._data

    def to_models(
        self, model: Callable[..., T], *, raise_if_empty: bool = False
    ) -> list[T] | None:
        """
        Converts all rows to a list of model instances.

        Args:
            model: A callable model class (e.g., Pydantic, dataclass).
            raise_if_empty: If True, raises ValueError when result is empty.

        Returns:
            A list of model instances, or None if empty and raise_if_empty is False.
        """
        if self.is_empty():
            if raise_if_empty:
                raise ValueError("Cannot convert empty result to models")
            return None
        return [model(**row) for row in self._data]

    def first(self) -> SingleQueryResult:
        """
        Returns the first row as a SingleQueryResult.
        If no data exists, returns an empty SingleQueryResult.
        """
        return (
            SingleQueryResult(self._data[0]) if self._data else SingleQueryResult(None)
        )

    def as_dicts(self) -> list[dict[str, Any]]:
        """
        Returns all result rows as a list of dictionaries.
        """
        return self._data

    def __iter__(self) -> Iterator[dict[str, Any]]:
        return iter(self._data)

    def __getitem__(self, idx: int) -> dict[str, Any]:
        return self._data[idx]

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, MultipleQueryResult) and self._data == other._data

    def __repr__(self) -> str:
        return f"<MultipleQueryResult {len(self._data)} rows>"
