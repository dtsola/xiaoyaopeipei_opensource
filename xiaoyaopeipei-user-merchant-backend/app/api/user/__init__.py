"""
C端API模块
"""
from fastapi import APIRouter
from app.api.user import chat, lead, shop

router = APIRouter()

# 注册子路由
router.include_router(chat.router, tags=["C端-对话"])
router.include_router(lead.router, tags=["C端-线索"])
router.include_router(shop.router, tags=["C端-店铺"])
