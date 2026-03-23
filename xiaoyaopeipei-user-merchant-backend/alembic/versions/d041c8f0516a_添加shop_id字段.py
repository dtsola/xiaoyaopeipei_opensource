"""添加shop_id字段

Revision ID: d041c8f0516a
Revises: 433fb9ddb36f
Create Date: 2026-01-23 10:15:41.909466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd041c8f0516a'
down_revision: Union[str, None] = '433fb9ddb36f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. 添加 shop_id 字段（检查是否已存在）
    from sqlalchemy import inspect
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('merchants')]

    if 'shop_id' not in columns:
        op.add_column('merchants', sa.Column('shop_id', sa.String(100), nullable=True))

        # 2. 为现有数据生成 shop_id（从 share_link 中提取）
        op.execute("""
            UPDATE merchants
            SET shop_id = share_link
        """)

        # 3. 设置 shop_id 为 NOT NULL
        op.alter_column('merchants', 'shop_id', nullable=False)

    # 4. 扩展 share_link 字段长度（从255到500，以存储完整URL）
    share_link_col = inspector.get_columns('merchants')
    current_length = next((c['type'].length for c in share_link_col if c['name'] == 'share_link'), None)
    if current_length and current_length < 500:
        op.alter_column('merchants', 'share_link', type_=sa.String(500))


def downgrade() -> None:
    # 1. 恢复 share_link 字段长度
    op.alter_column('merchants', 'share_link', type_=sa.String(255))

    # 2. 删除 shop_id 字段
    op.drop_column('merchants', 'shop_id')
