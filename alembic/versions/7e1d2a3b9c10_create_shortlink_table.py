"""create short_link partitioned table (final schema)

Revision ID: 7e1d2a3b9c10
Revises:
Create Date: 2026-04-30 23:50:00.000000

Replaces the former two-step chain (cb4c6c4208a1 + this revision).

The migration defines create_short_link_partition() only; invoking it (initial months and
ongoing) is scripts/create_short_link_partitions.py (e.g. after alembic upgrade head).

"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "7e1d2a3b9c10"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.text("DROP FUNCTION IF EXISTS create_short_link_partition"))

    op.execute(sa.text("""
            CREATE TABLE IF NOT EXISTS short_link (
                id UUID NOT NULL,
                short_code VARCHAR(32) NOT NULL,
                url TEXT NOT NULL,
                expires_at TIMESTAMPTZ NOT NULL,
                created_at TIMESTAMPTZ NOT NULL,
                is_custom BOOLEAN NOT NULL DEFAULT FALSE,
                UNIQUE (short_code, created_at),
                PRIMARY KEY (id, short_code, created_at)
            )
            PARTITION BY RANGE (created_at);
            """))

    op.execute(sa.text("""
            CREATE INDEX IF NOT EXISTS idx_short_link_short_code_and_created_at
            ON short_link (short_code, created_at DESC);
            """))

    op.execute(sa.text("""
            CREATE OR REPLACE FUNCTION create_short_link_partition(start_date TIMESTAMPTZ)
            RETURNS void AS $$
            DECLARE
                end_date TIMESTAMPTZ := start_date + INTERVAL '1 month';
                partition_name TEXT;
                hash_partition_name TEXT;
            BEGIN
                partition_name := 'short_link_' || to_char(start_date, 'YYYYMM');

                BEGIN
                    EXECUTE format(
                        'CREATE TABLE %I PARTITION OF short_link
                        FOR VALUES FROM (%L) TO (%L)
                        PARTITION BY HASH (short_code)',
                        partition_name, start_date, end_date
                    );
                EXCEPTION
                    WHEN duplicate_table THEN
                        NULL;
                END;

                FOR i IN 0..15 LOOP
                    hash_partition_name := partition_name || '_p' || lpad(i::text, 2, '0');

                    BEGIN
                        EXECUTE format(
                            'CREATE TABLE %I PARTITION OF %I
                            FOR VALUES WITH (MODULUS 16, REMAINDER %s)',
                            hash_partition_name, partition_name, i
                        );
                    EXCEPTION
                        WHEN duplicate_table THEN
                            NULL;
                    END;
                END LOOP;
            END;
            $$ LANGUAGE plpgsql;
            """))


def downgrade() -> None:
    op.execute(sa.text("DROP TABLE IF EXISTS short_link CASCADE"))
    op.execute(sa.text("DROP FUNCTION IF EXISTS create_short_link_partition"))
