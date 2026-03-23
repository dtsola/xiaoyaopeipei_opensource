"""添加会员到期时间字段

Revision ID: 20260123_add_membership_expiry
Revises: d041c8f0516a
Create Date: 2026-01-23 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta


# revision identifiers, used by Alembic.
revision: str = '20260123_add_membership_expiry'
down_revision: Union[str, None] = 'd041c8f0516a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. 添加 membership_expiry 字段
    op.add_column('merchants', sa.Column('membership_expiry', sa.DateTime(), nullable=True))

    # 2. 为现有用户设置会员到期时间（默认7天）
    seven_days_later = datetime.now() + timedelta(days=7)
    op.execute("""
        UPDATE merchants
        SET membership_expiry = '{}'
        WHERE membership_expiry IS NULL
    """.format(seven_days_later.strftime('%Y-%m-%d %H:%M:%S')))


def downgrade() -> None:
    # 删除 membership_expiry 字段
    op.drop_column('merchants', 'membership_expiry')
