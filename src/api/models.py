"""
API数据模型
"""
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime


class CrawlRequest(BaseModel):
    """爬取请求模型"""
    url: HttpUrl = Field(..., description="要爬取的URL")
    use_cache: bool = Field(default=True, description="是否使用缓存")
    
    
class CrawlResponse(BaseModel):
    """爬取响应模型"""
    success: bool = Field(..., description="是否成功")
    data: Optional[Dict[str, Any]] = Field(None, description="爬取的数据")
    error: Optional[str] = Field(None, description="错误信息")
    cached: bool = Field(default=False, description="是否来自缓存")
    

class SummaryRequest(BaseModel):
    """摘要请求模型"""
    content: str = Field(..., description="要摘要的内容")
    title: Optional[str] = Field(None, description="文章标题")
    use_cache: bool = Field(default=True, description="是否使用缓存")
    

class SummaryResponse(BaseModel):
    """摘要响应模型"""
    success: bool = Field(..., description="是否成功")
    summary: Optional[str] = Field(None, description="生成的摘要")
    error: Optional[str] = Field(None, description="错误信息")
    cached: bool = Field(default=False, description="是否来自缓存")
    

class AnalysisRequest(BaseModel):
    """分析请求模型"""
    content: str = Field(..., description="要分析的内容")
    title: Optional[str] = Field(None, description="文章标题")
    use_cache: bool = Field(default=True, description="是否使用缓存")
    

class AnalysisResponse(BaseModel):
    """分析响应模型"""
    success: bool = Field(..., description="是否成功")
    analysis: Optional[str] = Field(None, description="生成的分析")
    error: Optional[str] = Field(None, description="错误信息")
    cached: bool = Field(default=False, description="是否来自缓存")
    

class KeywordsRequest(BaseModel):
    """关键词请求模型"""
    content: str = Field(..., description="要提取关键词的内容")
    title: Optional[str] = Field(None, description="文章标题")
    use_cache: bool = Field(default=True, description="是否使用缓存")
    

class KeywordsResponse(BaseModel):
    """关键词响应模型"""
    success: bool = Field(..., description="是否成功")
    keywords: Optional[List[str]] = Field(None, description="提取的关键词")
    error: Optional[str] = Field(None, description="错误信息")
    cached: bool = Field(default=False, description="是否来自缓存")
    

class ProcessArticleRequest(BaseModel):
    """处理文章请求模型"""
    url: Optional[HttpUrl] = Field(None, description="文章URL（如果提供，会先爬取）")
    content: Optional[str] = Field(None, description="文章内容（直接提供）")
    title: Optional[str] = Field(None, description="文章标题")
    use_cache: bool = Field(default=True, description="是否使用缓存")
    
    def model_validate(cls, values):
        """验证至少提供URL或内容之一"""
        if not values.get('url') and not values.get('content'):
            raise ValueError('必须提供URL或内容之一')
        return values
        

class ProcessArticleResponse(BaseModel):
    """处理文章响应模型"""
    success: bool = Field(..., description="是否成功")
    data: Optional[Dict[str, Any]] = Field(None, description="处理后的数据")
    error: Optional[str] = Field(None, description="错误信息")
    cached: bool = Field(default=False, description="是否来自缓存")
    processing_time: Optional[float] = Field(None, description="处理时间（秒）")
    

class TLDRCrawlResponse(BaseModel):
    """TLDR爬取响应模型"""
    success: bool = Field(..., description="是否成功")
    data: Optional[Dict[str, Any]] = Field(None, description="爬取和处理后的数据")
    error: Optional[str] = Field(None, description="错误信息")
    cached: bool = Field(default=False, description="是否来自缓存")
    processing_time: Optional[float] = Field(None, description="处理时间（秒）")
    

class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str = Field(..., description="服务状态")
    timestamp: datetime = Field(..., description="检查时间")
    version: str = Field(..., description="版本号")
    services: Dict[str, str] = Field(..., description="各服务状态")
    

class ErrorResponse(BaseModel):
    """错误响应模型"""
    success: bool = Field(default=False, description="是否成功")
    error: str = Field(..., description="错误信息")
    error_code: Optional[str] = Field(None, description="错误代码")
    timestamp: datetime = Field(default_factory=datetime.now, description="错误时间")


class DatabaseContentResponse(BaseModel):
    """数据库内容响应模型"""
    success: bool = Field(..., description="是否成功")
    data: Optional[Dict[str, Any]] = Field(None, description="爬取内容数据")
    error: Optional[str] = Field(None, description="错误信息")


class DatabaseListResponse(BaseModel):
    """数据库内容列表响应模型"""
    success: bool = Field(..., description="是否成功")
    data: Optional[List[Dict[str, Any]]] = Field(None, description="内容列表")
    total: Optional[int] = Field(None, description="总数量")
    page: Optional[int] = Field(None, description="当前页码")
    limit: Optional[int] = Field(None, description="每页数量")
    error: Optional[str] = Field(None, description="错误信息")


class DatabaseStatsResponse(BaseModel):
    """数据库统计响应模型"""
    success: bool = Field(..., description="是否成功")
    stats: Optional[Dict[str, Any]] = Field(None, description="统计数据")
    error: Optional[str] = Field(None, description="错误信息")