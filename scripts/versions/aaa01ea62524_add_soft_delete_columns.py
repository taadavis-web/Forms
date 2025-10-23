"""add soft delete columns

Revision ID: aaa01ea62524
Revises: 
Create Date: 2025-10-23 09:11:48.458244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Integer, Column, Boolean, DateTime, false, func
from datetime import datetime, timezone


# revision identifiers, used by Alembic.
revision: str = 'aaa01ea62524'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("profile") as batch_op:
        batch_op.add_column(Column("deleted", Boolean, server_default=false()))

    with op.batch_alter_table("feedback") as batch_op:
        batch_op.add_column(Column("deleted", Boolean, server_default=false()))


def downgrade() -> None:
    with op.batch_alter_table("profile") as batch_op:
        batch_op.drop_column('deleted')
    with op.batch_alter_table("feedback") as batch_op:
        batch_op.drop_column('deleted')
