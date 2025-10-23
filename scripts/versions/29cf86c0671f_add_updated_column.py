"""add updated column

Revision ID: 29cf86c0671f
Revises: aaa01ea62524
Create Date: 2025-10-23 09:51:23.784569

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, DateTime, func


# revision identifiers, used by Alembic.
revision: str = '29cf86c0671f'
down_revision: Union[str, Sequence[str], None] = 'aaa01ea62524'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("profile") as batch_op:
        batch_op.add_column(Column("updated", DateTime, server_default=func.now()))

    with op.batch_alter_table("feedback") as batch_op:
        batch_op.add_column(Column("updated", DateTime, server_default=func.now()))


def downgrade() -> None:
    with op.batch_alter_table("profile") as batch_op:
        batch_op.drop_column('updated')
    with op.batch_alter_table("feedback") as batch_op:
        batch_op.drop_column('updated')
