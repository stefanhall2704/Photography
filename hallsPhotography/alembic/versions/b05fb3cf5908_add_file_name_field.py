"""Add file name field

Revision ID: b05fb3cf5908
Revises: 8c44dc046d31
Create Date: 2023-07-18 20:10:02.370533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b05fb3cf5908'
down_revision = '8c44dc046d31'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('Package', sa.Column('FileName', sa.String(200)))


def downgrade() -> None:
    op.drop_column('Package','FileName')
