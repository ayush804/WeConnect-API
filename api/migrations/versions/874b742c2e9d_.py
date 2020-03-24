"""empty message

Revision ID: 874b742c2e9d
Revises: 3734261bb209
Create Date: 2020-03-23 19:27:54.012962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '874b742c2e9d'
down_revision = '3734261bb209'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('WeConnect_Users',
    sa.Column('emailId', sa.Integer(), nullable=False),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.Column('creation_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('sex', sa.String(length=250), nullable=False),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('emailId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('WeConnect_Users')
    # ### end Alembic commands ###