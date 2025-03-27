from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a128588ab0cb'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # ### Add priority column with nullable=True ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('priority', sa.String(length=10), nullable=True))  # Make it nullable initially

    # ### Set default value for existing rows ###
    op.execute("UPDATE tasks SET priority = 'Medium' WHERE priority IS NULL")  # Set default value for existing tasks

    # ### Alter priority column to be NOT NULL ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('priority', nullable=False)  # Make it NOT NULL after updating rows

    # ### Ensure the user table's password_hash column exists ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=False))

def downgrade():
    # ### Remove the password_hash column from the user table ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('password_hash')

    # ### Drop the priority column from the tasks table ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.drop_column('priority')
