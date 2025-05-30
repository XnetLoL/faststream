import warnings
from typing import Optional

from faststream.broker.schemas import NameRequired
from faststream.exceptions import SetupError


class StreamSub(NameRequired):
    """A class to represent a Redis Stream subscriber."""

    __slots__ = (
        "batch",
        "consumer",
        "group",
        "last_id",
        "max_concurrent",
        "max_records",
        "maxlen",
        "name",
        "no_ack",
        "polling_interval",
    )

    def __init__(
        self,
        stream: str,
        polling_interval: Optional[int] = 100,
        group: Optional[str] = None,
        consumer: Optional[str] = None,
        batch: bool = False,
        no_ack: bool = False,
        last_id: Optional[str] = None,
        maxlen: Optional[int] = None,
        max_records: Optional[int] = None,
        max_concurrent: Optional[int] = None,
    ) -> None:
        if (group and not consumer) or (not group and consumer):
            raise SetupError("You should specify `group` and `consumer` both")

        if group and consumer and no_ack:
            warnings.warn(
                message="`no_ack` has no effect with consumer group",
                category=RuntimeWarning,
                stacklevel=1,
            )

        if last_id is None:
            last_id = "$"

        super().__init__(stream)

        self.group = group
        self.consumer = consumer
        self.polling_interval = polling_interval
        self.batch = batch
        self.no_ack = no_ack
        self.last_id = last_id
        self.maxlen = maxlen
        self.max_records = max_records
        self.max_concurrent = max_concurrent

    def __hash__(self) -> int:
        if self.group is not None:
            return hash(
                f"stream:{self.name} group:{self.group} consumer:{self.consumer}"
            )
        return hash(f"stream:{self.name}")
