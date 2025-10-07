"""
数据库模型定义
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import json


class Article(BaseModel):
    """单篇文章模型"""
    title: str
    content: str
    links: List[Dict[str, str]] = []
    word_count: int = 0
    reading_time: Optional[str] = None


class Section(BaseModel):
    """分类模型"""
    title: str
    articles: List[Article] = []
    article_count: int = 0


class CrawledContent(BaseModel):
    """爬取内容的完整模型"""
    id: Optional[int] = None
    url: str
    title: str
    subtitle: Optional[str] = None
    content: str
    meta_description: Optional[str] = None
    articles: List[Article] = []
    sections: List[Section] = []
    external_links: List[Dict[str, str]] = []
    crawled_at: datetime = Field(default_factory=datetime.now)
    word_count: int = 0
    article_count: int = 0
    # 处理状态字段
    is_crawled: bool = False  # 是否完成爬取
    is_ai_processed: bool = False  # 是否完成AI处理
    processing_status: str = "pending"  # pending, crawled, ai_processed, completed
    # AI处理结果字段
    summary: Optional[str] = None  # AI生成的摘要
    analysis: Optional[str] = None  # AI生成的分析
    keywords: List[str] = []  # AI提取的关键词
    references: List[Dict[str, Any]] = []  # AI提取的引用信息
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式，用于数据库存储"""
        data = self.dict()
        # 将复杂对象转换为JSON字符串
        data['articles'] = json.dumps([article.dict() for article in self.articles])
        data['sections'] = json.dumps([section.dict() for section in self.sections])
        data['external_links'] = json.dumps(self.external_links)
        data['keywords'] = json.dumps(self.keywords)
        data['references'] = json.dumps(self.references)
        data['crawled_at'] = self.crawled_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CrawledContent':
        """从字典创建对象，用于数据库读取"""
        # 解析JSON字符串
        if isinstance(data.get('articles'), str):
            articles_data = json.loads(data['articles'])
            data['articles'] = [Article(**article) for article in articles_data]
        
        if isinstance(data.get('sections'), str):
            sections_data = json.loads(data['sections'])
            data['sections'] = [Section(**section) for section in sections_data]
        
        if isinstance(data.get('external_links'), str):
            data['external_links'] = json.loads(data['external_links'])
        
        if isinstance(data.get('keywords'), str):
            data['keywords'] = json.loads(data['keywords'])
        
        if isinstance(data.get('references'), str):
            data['references'] = json.loads(data['references'])
        
        if isinstance(data.get('crawled_at'), str):
            data['crawled_at'] = datetime.fromisoformat(data['crawled_at'])
        
        return cls(**data)


class CrawlStats(BaseModel):
    """爬取统计信息"""
    total_crawls: int = 0
    successful_crawls: int = 0
    failed_crawls: int = 0
    total_articles: int = 0
    last_crawl_time: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }