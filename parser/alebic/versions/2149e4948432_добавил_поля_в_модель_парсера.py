"""добавил поля в модель парсера

Revision ID: 2149e4948432
Revises: ad669366a757
Create Date: 2024-02-28 00:42:32.126231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2149e4948432'
down_revision: Union[str, None] = 'ad669366a757'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
