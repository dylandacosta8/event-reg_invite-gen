"""invitation_model

Revision ID: c7ef6b0a2cb9
Revises: 25d814bc83ed
Create Date: 2024-11-11 04:59:24.442179

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7ef6b0a2cb9'
down_revision: Union[str, None] = '25d814bc83ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'invitations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('invitee_email', sa.String(length=255), nullable=False),
        sa.Column('invite_code', sa.String(), nullable=False),
        sa.Column('user_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text("timezone('utc', now())")),
        sa.Column('used', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('nickname', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('invite_code'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invitations')
    # ### end Alembic commands ###
