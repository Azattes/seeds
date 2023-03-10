import uuid
from datetime import datetime

import ormar
from dependencies import get_database, get_metadata
from pydantic.typing import ForwardRef

SeedRef = ForwardRef("Seed")


class BaseMeta(ormar.ModelMeta):
    database = get_database()
    metadata = get_metadata()


class Seed(ormar.Model):
    class Meta(BaseMeta):
        tablename = "seeds"

    id: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4)
    is_executed: bool = ormar.Boolean(default=False)
    previous_seed_id: SeedRef = ormar.ForeignKey(
        SeedRef,
        nullable=True,
        ondelete=ormar.ReferentialAction.CASCADE,
        related_name="previous",
    )
    created_at: datetime = ormar.DateTime(
        default=datetime.utcnow, timezone=True
    )


Seed.update_forward_refs()
