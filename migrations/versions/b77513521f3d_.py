"""empty message

Revision ID: b77513521f3d
Revises: 7f9dd2471f2b
Create Date: 2020-08-17 08:35:15.868200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b77513521f3d'
down_revision = '7f9dd2471f2b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('games',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('gold_earn', sa.Float(), nullable=False),
    sa.Column('gold_spent_worker', sa.Float(), nullable=False),
    sa.Column('gold_spent_army', sa.Float(), nullable=False),
    sa.Column('new_person_cost', sa.Float(), nullable=False),
    sa.Column('win_probability', sa.Float(), nullable=False),
    sa.Column('rob_default_probability', sa.Float(), nullable=False),
    sa.Column('rob_extra_probability', sa.Float(), nullable=False),
    sa.Column('enemy_gold', sa.Float(), nullable=False),
    sa.Column('enemy_increase', sa.Float(), nullable=False),
    sa.Column('enemy_decrease', sa.Float(), nullable=False),
    sa.Column('uncertain_gold', sa.Float(), nullable=False),
    sa.Column('uncertain_population', sa.Float(), nullable=False),
    sa.Column('uncertain_army', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('states',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('gold', sa.Integer(), nullable=False),
    sa.Column('population', sa.Integer(), nullable=False),
    sa.Column('army', sa.Integer(), nullable=False),
    sa.Column('enemies', sa.Integer(), nullable=False),
    sa.Column('notifications', sa.Text(), nullable=False),
    sa.Column('reaction_move', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('states')
    op.drop_table('settings')
    op.drop_table('games')
    # ### end Alembic commands ###