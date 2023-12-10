"""diagnose

Revision ID: 01db30e0aa02
Revises: 58f7d9386e12
Create Date: 2023-12-10 23:10:16.517607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01db30e0aa02'
down_revision: Union[str, None] = '58f7d9386e12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('diagnoses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_diagnoses_id'), 'diagnoses', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_diagnoses_id'), table_name='diagnoses')
    op.drop_table('diagnoses')
    # ### end Alembic commands ###