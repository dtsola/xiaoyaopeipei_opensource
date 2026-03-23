"""
分享Schema
"""
from typing import Optional, Dict
from pydantic import BaseModel, Field


class QrcodeResponse(BaseModel):
    """二维码响应Schema"""

    qrcode_url: str = Field(..., description="二维码URL")
    share_link: str = Field(..., description="分享链接")


class PosterRequest(BaseModel):
    """生成海报请求Schema"""

    template_id: str = Field(..., description="模板ID（template_1/template_2/template_3）")


class PosterResponse(BaseModel):
    """生成海报响应Schema"""

    poster_url: str = Field(..., description="海报URL")


class StatsResponse(BaseModel):
    """分享统计响应Schema"""

    scan_count: int = Field(..., description="扫码数")
    consult_count: int = Field(..., description="咨询数")
    lead_count: int = Field(..., description="线索数")
    conversion_rate: float = Field(..., description="转化率")
    device_type_stats: Dict[str, int] = Field(..., description="设备类型统计")
    budget_stats: Dict[str, int] = Field(..., description="预算分布统计")
