"""create package table

Revision ID: 8c44dc046d31
Revises: 
Create Date: 2023-07-15 20:44:09.422743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c44dc046d31'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'Package',
        sa.Column('ID', sa.Integer, primary_key=True, nullable=False),
        sa.Column('Name', sa.String(100), nullable=False),
        sa.Column('TimeFrame', sa.String(50), nullable=False),
        sa.Column('Price', sa.Float, nullable=False)
    )

def downgrade() -> None:
    op.drop_table('Package')
