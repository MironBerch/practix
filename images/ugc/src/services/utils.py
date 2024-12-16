from uuid import UUID

from bson.binary import Binary


def to_binary(value: UUID) -> Binary:
    """Convert `UUID` to MongoDB binary format."""
    return Binary(value.bytes)
