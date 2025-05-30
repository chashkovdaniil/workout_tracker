"""description of changes

Revision ID: 89489902da6f
Revises: 93cd52b5b10b
Create Date: 2025-05-08 20:46:47.198433+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89489902da6f'
down_revision: Union[str, None] = '93cd52b5b10b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('fki_user_id_fkey', table_name='exercises')
    op.drop_constraint('user_id_fkey', 'exercises', type_='foreignkey')
    op.create_foreign_key(None, 'exercises', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'exercises', type_='foreignkey')
    op.create_foreign_key('user_id_fkey', 'exercises', 'users', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_index('fki_user_id_fkey', 'exercises', ['user_id'], unique=False)
    # ### end Alembic commands ###
