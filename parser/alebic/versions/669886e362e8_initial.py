"""Initial

Revision ID: 669886e362e8
Revises: 
Create Date: 2024-03-04 13:46:37.078338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from app.models.fields import Json

# revision identifiers, used by Alembic.
revision: str = '669886e362e8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bs4_parsers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('search_by_attrs', Json(), nullable=True),
    sa.Column('output_attrs', postgresql.ARRAY(sa.String()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('endpoints',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('headers', Json(), nullable=True),
    sa.Column('params', Json(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('regexp_parsers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('regexp', sa.String(), nullable=False),
    sa.Column('type', postgresql.ENUM('DICT', 'FIND_ALL', name='type'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time_delay', sa.Integer(), nullable=False),
    sa.Column('last_check_time', sa.DateTime(), nullable=True),
    sa.Column('send_result_url', sa.String(), nullable=False),
    sa.Column('endpoint_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['endpoint_id'], ['endpoints.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('checks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('result', Json(), nullable=True),
    sa.Column('rule', sa.Integer(), nullable=True),
    sa.Column('status', postgresql.ENUM('NEW', 'IN_PROGRESS', name='status'), nullable=False),
    sa.ForeignKeyConstraint(['rule'], ['rules.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('parsers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parser_type', postgresql.ENUM('REGEXP_PARSER', 'BS4_PARSER', name='parser_type'), nullable=False),
    sa.Column('parser_id', sa.Integer(), nullable=True),
    sa.Column('rule_id', sa.Integer(), nullable=True),
    sa.Column('list_input', sa.Boolean(), nullable=True),
    sa.Column('linerize_result', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['rule_id'], ['rules.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('parsers')
    op.drop_table('checks')
    op.drop_table('rules')
    op.drop_table('regexp_parsers')
    op.drop_table('endpoints')
    op.drop_table('bs4_parsers')
    # ### end Alembic commands ###