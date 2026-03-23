"""
雪花算法ID生成器测试
"""
from app.utils.snowflake import generate_id


def test_generate_id():
    """测试生成雪花ID"""
    id1 = generate_id()
    id2 = generate_id()

    # 验证ID是20位整数
    assert len(str(id1)) == 20
    assert len(str(id2)) == 20

    # 验证ID唯一性
    assert id1 != id2

    # 验证ID递增
    assert id2 > id1
