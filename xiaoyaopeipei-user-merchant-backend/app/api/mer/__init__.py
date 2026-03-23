"""
B端API模块
"""
from fastapi import APIRouter
from app.api.mer import auth, sku, lead, share, upload, dashboard

router = APIRouter()

# 注册子路由
router.include_router(auth.router, tags=["B端-认证"])
router.include_router(sku.router, tags=["B端-SKU"])
router.include_router(lead.router, tags=["B端-线索"])
router.include_router(share.router, tags=["B端-分享"])
router.include_router(upload.router, tags=["B端-上传"])
router.include_router(dashboard.router, tags=["B端-看板"])
