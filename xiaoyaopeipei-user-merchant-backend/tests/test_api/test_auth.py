"""
认证接口测试
"""
import pytest


def test_register(client):
    """测试商家注册"""
    response = client.post(
        "/api/mer/auth/register",
        json={
            "username": "testuser",
            "password": "Password123!",
            "shop_name": "测试店铺",
            "phone": "13812345678",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "token" in data["data"]


def test_login(client):
    """测试商家登录"""
    # 先注册
    client.post(
        "/api/mer/auth/register",
        json={
            "username": "testuser2",
            "password": "Password123!",
            "shop_name": "测试店铺",
            "phone": "13812345678",
        },
    )

    # 再登录
    response = client.post(
        "/api/mer/auth/login",
        json={"username": "testuser2", "password": "Password123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "token" in data["data"]
