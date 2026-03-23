"""
对话Schema
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    """发送消息请求Schema"""

    session_id: Optional[str] = Field(None, description="会话ID（首次传空）")
    shop_id: str = Field(..., description="店铺ID")
    message: str = Field(..., min_length=1, max_length=500, description="用户消息内容")


class ExtractedInfo(BaseModel):
    """AI提取的信息"""

    budget: Optional[str] = Field(None, description="预算")
    device_type: Optional[str] = Field(None, description="设备类型")
    usage: Optional[str] = Field(None, description="用途")
    requirements: Optional[str] = Field(None, description="具体需求")
    brand: Optional[str] = Field(None, description="品牌偏好")
    portable: Optional[str] = Field(None, description="便携性需求")


class ChatMessageResponse(BaseModel):
    """发送消息响应Schema"""

    session_id: str = Field(..., description="会话ID")
    ai_response: str = Field(..., description="AI回复内容")
    extracted_info: ExtractedInfo = Field(..., description="AI提取的用户需求信息")
    is_complete: bool = Field(..., description="信息是否收集完整")
    next_action: str = Field(..., description="下一步动作（ask/recommend）")
    quick_replies: List[str] = Field(default_factory=list, description="快捷回复选项")


class RecommendationRequest(BaseModel):
    """获取推荐方案请求Schema"""

    session_id: str = Field(..., description="会话ID")
    shop_id: str = Field(..., description="店铺ID")
    needs: ExtractedInfo = Field(..., description="用户需求信息")


class SkuSpecs(BaseModel):
    """SKU配置参数"""

    cpu: str = Field(..., description="处理器")
    gpu: Optional[str] = Field(None, description="显卡")
    ram: str = Field(..., description="内存")
    storage: str = Field(..., description="存储")
    screen: Optional[str] = Field(None, description="屏幕")
    weight: Optional[str] = Field(None, description="重量")
    battery: Optional[str] = Field(None, description="续航")


class RecommendationItem(BaseModel):
    """推荐方案项Schema"""

    sku_id: str = Field(..., description="配置ID")
    name: str = Field(..., description="配置名称")
    device_type: str = Field(..., description="设备类型")
    brand: str = Field(..., description="品牌")
    price: float = Field(..., description="价格")
    specs: SkuSpecs = Field(..., description="配置参数")
    images: List[str] = Field(default_factory=list, description="图片URL数组")
    ai_reason: str = Field(..., description="AI推荐理由")
    match_score: int = Field(..., description="匹配分数（0-100）")


class RecommendationResponse(BaseModel):
    """获取推荐方案响应Schema"""

    recommendations: List[RecommendationItem] = Field(..., description="推荐方案列表")
