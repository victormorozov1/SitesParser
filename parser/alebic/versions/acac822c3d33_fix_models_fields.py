"""fix models fields

Revision ID: acac822c3d33
Revises: 669886e362e8
Create Date: 2024-03-10 22:28:21.217125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'acac822c3d33'
down_revision: Union[str, None] = '669886e362e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bs4_parsers', sa.Column('list_input', sa.Boolean(), nullable=True))
    op.add_column('bs4_parsers', sa.Column('linerize_result', sa.Boolean(), nullable=True))
    op.drop_column('parsers', 'linerize_result')
    op.drop_column('parsers', 'list_input')
    op.add_column('regexp_parsers', sa.Column('list_input', sa.Boolean(), nullable=True))
    op.add_column('regexp_parsers', sa.Column('linerize_result', sa.Boolean(), nullable=True))
    op.drop_column('rules', 'time_delay')
    op.drop_column('rules', 'send_result_url')
    op.drop_column('rules', 'last_check_time')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rules', sa.Column('last_check_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('rules', sa.Column('send_result_url', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('rules', sa.Column('time_delay', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('regexp_parsers', 'linerize_result')
    op.drop_column('regexp_parsers', 'list_input')
    op.add_column('parsers', sa.Column('list_input', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('parsers', sa.Column('linerize_result', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('bs4_parsers', 'linerize_result')
    op.drop_column('bs4_parsers', 'list_input')
    # ### end Alembic commands ###
