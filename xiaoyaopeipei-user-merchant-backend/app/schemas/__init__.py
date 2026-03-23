"""
Schema模块
"""
from app.schemas.base import (
    ResponseSchema,
    PaginationSchema,
    PaginationParams,
)
from app.schemas.merchant import (
    MerchantBase,
    MerchantCreate,
    MerchantUpdate,
    MerchantResponse,
    MerchantLogin,
    MerchantAuthResponse,
)
from app.schemas.sku import (
    SkuBase,
    SkuCreate,
    SkuUpdate,
    SkuResponse,
    SkuListItem,
)
from app.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    RecommendationRequest,
    RecommendationResponse,
    ExtractedInfo,
)
from app.schemas.lead import (
    LeadSubmitRequest,
    LeadSubmitResponse,
    LeadNote,
    LeadStatusUpdate,
    LeadListItem,
    LeadDetail,
)
from app.schemas.share import (
    QrcodeResponse,
    PosterRequest,
    PosterResponse,
    StatsResponse,
)

__all__ = [
    "ResponseSchema",
    "PaginationSchema",
    "PaginationParams",
    "MerchantBase",
    "MerchantCreate",
    "MerchantUpdate",
    "MerchantResponse",
    "MerchantLogin",
    "MerchantAuthResponse",
    "SkuBase",
    "SkuCreate",
    "SkuUpdate",
    "SkuResponse",
    "SkuListItem",
    "ChatMessageRequest",
    "ChatMessageResponse",
    "RecommendationRequest",
    "RecommendationResponse",
    "ExtractedInfo",
    "LeadSubmitRequest",
    "LeadSubmitResponse",
    "LeadNote",
    "LeadStatusUpdate",
    "LeadListItem",
    "LeadDetail",
    "QrcodeResponse",
    "PosterRequest",
    "PosterResponse",
    "StatsResponse",
]
