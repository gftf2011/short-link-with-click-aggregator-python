"""create click partitioned table

Revision ID: b3c4d5e6f7a8
Revises: 7e1d2a3b9c10
Create Date: 2026-05-21 00:00:00.000000

Hash-partitioned by short_code (MODULUS 16). All 16 partitions are static
and created here — no periodic script needed unlike short_link's range partitions.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "b3c4d5e6f7a8"
down_revision: Union[str, Sequence[str], None] = "7e1d2a3b9c10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_MODULUS = 16


def upgrade() -> None:
    op.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS click (
            short_code VARCHAR(32) NOT NULL,
            count      BIGINT      NOT NULL DEFAULT 0,
            PRIMARY KEY (short_code)
        ) PARTITION BY HASH (short_code)
    """))

    for i in range(_MODULUS):
        op.execute(sa.text(
            f"CREATE TABLE IF NOT EXISTS click_p{i:02d}"
            f" PARTITION OF click"
            f" FOR VALUES WITH (MODULUS {_MODULUS}, REMAINDER {i})"
        ))

    op.execute(sa.text("""
        CREATE INDEX IF NOT EXISTS idx_click_short_code ON click (short_code)
    """))


def downgrade() -> None:
    op.execute(sa.text("DROP TABLE IF EXISTS click CASCADE"))
