"""empty message

Revision ID: a1e73a8d2bf8
Revises: bf2637e1f4c2
Create Date: 2024-05-03 18:07:01.261405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1e73a8d2bf8'
down_revision = 'bf2637e1f4c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('professor',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.Column('idade', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('professor')
    # ### end Alembic commands ###
