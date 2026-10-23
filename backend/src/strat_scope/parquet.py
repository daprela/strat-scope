"""Lossless strings at the PyArrow boundary; no monetary arithmetic policy."""

import importlib
from typing import Protocol, cast

from strat_scope.wire import ExactObservation


class Table(Protocol):
    def to_pydict(self) -> dict[str, list[object]]: ...


class Buffer(Protocol):
    def to_pybytes(self) -> bytes: ...


class Sink(Protocol):
    def getvalue(self) -> Buffer: ...


class Arrow(Protocol):
    def string(self) -> object: ...
    def schema(self, fields: list[tuple[str, object]]) -> object: ...
    def table(self, data: dict[str, list[str]], schema: object) -> Table: ...
    def BufferOutputStream(self) -> Sink: ...
    def BufferReader(self, payload: bytes) -> object: ...


class Parquet(Protocol):
    def write_table(self, table: Table, sink: Sink) -> None: ...
    def read_table(self, source: object) -> Table: ...


def encode(rows: list[ExactObservation]) -> bytes:
    # These narrow protocols isolate PyArrow's untyped extension surface.
    arrow = cast(Arrow, importlib.import_module("pyarrow"))
    parquet = cast(Parquet, importlib.import_module("pyarrow.parquet"))
    fields = ["instant", "unit", "occurrence", "value"]
    data = {field: [str(getattr(row, field)) for row in rows] for field in fields}
    table = arrow.table(data, arrow.schema([(name, arrow.string()) for name in fields]))
    sink = arrow.BufferOutputStream()
    parquet.write_table(table, sink)
    return sink.getvalue().to_pybytes()


def decode(payload: bytes) -> list[ExactObservation]:
    arrow = cast(Arrow, importlib.import_module("pyarrow"))
    parquet = cast(Parquet, importlib.import_module("pyarrow.parquet"))
    data = parquet.read_table(arrow.BufferReader(payload)).to_pydict()
    if set(data) != {"instant", "unit", "occurrence", "value"}:
        raise ValueError("unexpected precision schema")
    length = len(data["instant"])
    if any(len(column) != length for column in data.values()):
        raise ValueError("invalid column lengths")
    return [
        ExactObservation.model_validate(
            {key: values[i] for key, values in data.items()}
        )
        for i in range(length)
    ]
