"""
API路由定义
"""
import time
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from .models import (
    CrawlRequest, CrawlResponse,
    SummaryRequest, SummaryResponse,
    AnalysisRequest, AnalysisResponse,
    KeywordsRequest, KeywordsResponse,
    ProcessArticleRequest, ProcessArticleResponse,
    TLDRCrawlResponse, HealthResponse, ErrorResponse,
    DatabaseContentResponse, DatabaseListResponse, DatabaseStatsResponse
)
from src.crawler import WebCrawler
from src.ai import AzureOpenAIClient
from src.utils.data_converter import DataConverter
from src.database.models import Article, Section
from src.database import DatabaseManager, CrawledContent
from src.utils import cache_manager
from config import settings, app_logger

# 创建路由器
router = APIRouter()

# 全局实例
ai_client = AzureOpenAIClient()
db_manager = DatabaseManager()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查端点"""
    try:
        # 检查各个服务状态
        services = {
            "api": "healthy",
            "cache": "healthy" if cache_manager.redis_client else "unavailable",
            "azure_openai": "healthy",
            "crawler": "healthy"
        }
        
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now(),
            version="1.0.0",
            services=services
        )
    except Exception as e:
        app_logger.error(f"健康检查失败: {e}")
        raise HTTPException(status_code=500, detail="服务不可用")


@router.post("/crawl", response_model=CrawlResponse)
async def crawl_url(request: CrawlRequest):
    """爬取指定URL"""
    try:
        url = str(request.url)
        app_logger.info(f"收到爬取请求: {url}")
        
        # 检查缓存
        if request.use_cache:
            cached_data = await cache_manager.get_crawl_cache(url)
            if cached_data:
                app_logger.info(f"返回缓存数据: {url}")
                return CrawlResponse(
                    success=True,
                    data=cached_data,
                    cached=True
                )
        
        # 执行爬取
        async with WebCrawler() as crawler:
            data = await crawler.crawl_url(url)
            
        if data is None:
            return CrawlResponse(
                success=False,
                error="爬取失败，请检查URL是否有效"
            )
            
        # 缓存结果
        if request.use_cache:
            await cache_manager.set_crawl_cache(url, data)
            
        return CrawlResponse(
            success=True,
            data=data,
            cached=False
        )
        
    except Exception as e:
        app_logger.error(f"爬取请求处理失败: {e}")
        return CrawlResponse(
            success=False,
            error=f"爬取失败: {str(e)}"
        )


@router.post("/summary", response_model=SummaryResponse)
async def generate_summary(request: SummaryRequest):
    """生成文章摘要"""
    try:
        app_logger.info("收到摘要生成请求")
        
        # 检查缓存
        if request.use_cache:
            cached_summary = await cache_manager.get_ai_cache(
                request.content, "summary"
            )
            if cached_summary:
                app_logger.info("返回缓存的摘要")
                return SummaryResponse(
                    success=True,
                    summary=cached_summary,
                    cached=True
                )
        
        # 生成摘要
        summary = await ai_client.generate_summary(
            request.content, request.title or ""
        )
        
        if summary is None:
            return SummaryResponse(
                success=False,
                error="摘要生成失败"
            )
            
        # 缓存结果
        if request.use_cache:
            await cache_manager.set_ai_cache(
                request.content, "summary", summary
            )
            
        return SummaryResponse(
            success=True,
            summary=summary,
            cached=False
        )
        
    except Exception as e:
        app_logger.error(f"摘要生成失败: {e}")
        return SummaryResponse(
            success=False,
            error=f"摘要生成失败: {str(e)}"
        )


@router.post("/analysis", response_model=AnalysisResponse)
async def generate_analysis(request: AnalysisRequest):
    """生成深度分析"""
    try:
        app_logger.info("收到分析生成请求")
        
        # 检查缓存
        if request.use_cache:
            cached_analysis = await cache_manager.get_ai_cache(
                request.content, "analysis"
            )
            if cached_analysis:
                app_logger.info("返回缓存的分析")
                return AnalysisResponse(
                    success=True,
                    analysis=cached_analysis,
                    cached=True
                )
        
        # 生成分析
        analysis = await ai_client.generate_analysis(
            request.content, request.title or ""
        )
        
        if analysis is None:
            return AnalysisResponse(
                success=False,
                error="分析生成失败"
            )
            
        # 缓存结果
        if request.use_cache:
            await cache_manager.set_ai_cache(
                request.content, "analysis", analysis
            )
            
        return AnalysisResponse(
            success=True,
            analysis=analysis,
            cached=False
        )
        
    except Exception as e:
        app_logger.error(f"分析生成失败: {e}")
        return AnalysisResponse(
            success=False,
            error=f"分析生成失败: {str(e)}"
        )


@router.post("/keywords", response_model=KeywordsResponse)
async def extract_keywords(request: KeywordsRequest):
    """提取关键词"""
    try:
        app_logger.info("收到关键词提取请求")
        
        # 检查缓存
        if request.use_cache:
            cached_keywords = await cache_manager.get_ai_cache(
                request.content, "keywords"
            )
            if cached_keywords:
                app_logger.info("返回缓存的关键词")
                # 缓存中的关键词是字符串，需要转换为列表
                keywords_list = cached_keywords.split(',') if isinstance(cached_keywords, str) else cached_keywords
                return KeywordsResponse(
                    success=True,
                    keywords=keywords_list,
                    cached=True
                )
        
        # 提取关键词
        keywords = await ai_client.generate_keywords(
            request.content, request.title or ""
        )
        
        if keywords is None:
            return KeywordsResponse(
                success=False,
                error="关键词提取失败"
            )
            
        # 缓存结果
        if request.use_cache:
            await cache_manager.set_ai_cache(
                request.content, "keywords", ','.join(keywords)
            )
            
        return KeywordsResponse(
            success=True,
            keywords=keywords,
            cached=False
        )
        
    except Exception as e:
        app_logger.error(f"关键词提取失败: {e}")
        return KeywordsResponse(
            success=False,
            error=f"关键词提取失败: {str(e)}"
        )


@router.post("/process", response_model=ProcessArticleResponse)
async def process_article(request: ProcessArticleRequest):
    """处理文章（爬取+AI处理）"""
    start_time = time.time()
    
    try:
        app_logger.info("收到文章处理请求")
        
        # 获取文章数据
        if request.url:
            # 从URL爬取
            url = str(request.url)
            
            # 检查爬取缓存
            if request.use_cache:
                cached_data = await cache_manager.get_crawl_cache(url)
                if cached_data:
                    article_data = cached_data
                    app_logger.info(f"使用缓存的爬取数据: {url}")
                else:
                    async with WebCrawler() as crawler:
                        article_data = await crawler.crawl_url(url)
                    if article_data:
                        await cache_manager.set_crawl_cache(url, article_data)
            else:
                async with WebCrawler() as crawler:
                    article_data = await crawler.crawl_url(url)
                    
            if article_data is None:
                return ProcessArticleResponse(
                    success=False,
                    error="爬取失败，请检查URL是否有效"
                )
        else:
            # 直接使用提供的内容
            article_data = {
                'content': request.content,
                'title': request.title or '',
                'url': '',
                'word_count': len(request.content.split()),
                'crawled_at': time.time()
            }
        
        # AI处理
        processed_data = await ai_client.process_article(article_data)
        
        processing_time = time.time() - start_time
        
        return ProcessArticleResponse(
            success=True,
            data=processed_data,
            cached=False,
            processing_time=processing_time
        )
        
    except Exception as e:
        app_logger.error(f"文章处理失败: {e}")
        return ProcessArticleResponse(
            success=False,
            error=f"文章处理失败: {str(e)}",
            processing_time=time.time() - start_time
        )


@router.get("/tldr", response_model=TLDRCrawlResponse)
async def crawl_tldr_ai(url: str = None, force_refresh: bool = False):
    """爬取TLDR AI页面并进行AI处理"""
    start_time = time.time()
    
    try:
        app_logger.info("开始爬取TLDR AI页面")
        
        # 检查数据库中是否已存在
        target_url = url if url else settings.crawler.target_url
        existing_content = db_manager.get_crawled_content(target_url)
        
        # 如果强制刷新，跳过缓存检查
        if not force_refresh and existing_content:
            # 检查处理状态
            if getattr(existing_content, 'processing_status', 'completed') == 'completed' or \
               getattr(existing_content, 'is_ai_processed', True):
                app_logger.info("返回数据库中已完全处理的TLDR数据")
                # 构建返回数据格式
                processed_data = {
                    'url': existing_content.url,
                    'title': existing_content.title,
                    'subtitle': existing_content.subtitle,
                    'content': existing_content.content,
                    'meta_description': existing_content.meta_description,
                    'articles': [article.dict() for article in existing_content.articles],
                    'sections': existing_content.sections,
                    'word_count': existing_content.word_count,
                    'article_count': existing_content.article_count,
                    'crawled_at': existing_content.crawled_at.isoformat(),
                    'database_id': existing_content.id,
                    'processing_status': getattr(existing_content, 'processing_status', 'completed'),
                    # 添加AI处理结果
                    'summary': getattr(existing_content, 'summary', None),
                    'analysis': getattr(existing_content, 'analysis', None),
                    'keywords': getattr(existing_content, 'keywords', []),
                    'references': getattr(existing_content, 'references', [])
                }
                return TLDRCrawlResponse(
                    success=True,
                    data=processed_data,
                    cached=True,
                    processing_time=time.time() - start_time
                )
            elif getattr(existing_content, 'is_crawled', False) and \
                 not getattr(existing_content, 'is_ai_processed', False):
                app_logger.info("发现已爬取但未AI处理的内容，继续AI处理")
                # 直接进行AI处理，跳过爬取步骤
                article_data = {
                    'title': existing_content.title,
                    'subtitle': existing_content.subtitle,
                    'content': existing_content.content,
                    'meta_description': existing_content.meta_description,
                    'articles': [article.dict() for article in existing_content.articles],
                    'sections': existing_content.sections,
                    'word_count': existing_content.word_count,
                    'article_count': existing_content.article_count
                }
                # 跳转到AI处理步骤
                processed_data = await ai_client.process_article(article_data)
                
                # 使用 DataConverter 更新AI处理结果
                DataConverter.update_with_ai_results(existing_content, processed_data)
                db_manager.save_crawled_content(existing_content)
                
                app_logger.info(f"完成AI处理，更新数据库记录")
                
                processed_data['database_id'] = existing_content.id
                processed_data['processing_status'] = 'completed'
                return TLDRCrawlResponse(
                    success=True,
                    data=processed_data,
                    cached=False,
                    processing_time=time.time() - start_time
                )
        
        # 爬取页面
        async with WebCrawler() as crawler:
            article_data = await crawler.crawl_tldr_ai(target_url)
            
        if article_data is None:
            return TLDRCrawlResponse(
                success=False,
                error="TLDR AI页面爬取失败"
            )
        
        # 先保存爬取的原始数据（状态：已爬取，未AI处理）
        crawled_content = None  # 初始化变量
        try:
            # 使用 DataConverter 转换爬虫数据为模型对象
            crawled_content = DataConverter.convert_crawled_data_to_model(
                article_data=article_data,
                target_url=target_url,
                processing_status='crawled'
            )
            
            # 保存爬取阶段的数据
            content_id = db_manager.save_crawled_content(crawled_content)
            app_logger.info(f"成功保存爬取内容到数据库，ID: {content_id}")
            
        except Exception as db_error:
            app_logger.error(f"保存爬取数据到数据库失败: {db_error}")
            # 不影响主流程，继续AI处理
        
        # AI处理
        app_logger.info("开始AI处理")
        processed_data = await ai_client.process_article(article_data)
        
        # 更新数据库，保存AI处理结果
        try:
            if crawled_content is not None:
                # 使用 DataConverter 更新AI处理结果
                DataConverter.update_with_ai_results(crawled_content, processed_data)
                
                # 更新数据库记录
                content_id = db_manager.save_crawled_content(crawled_content)
                app_logger.info(f"成功保存AI处理结果到数据库，ID: {content_id}")
                
                # 在返回数据中添加数据库ID和状态
                processed_data['database_id'] = content_id
                processed_data['processing_status'] = 'completed'
            else:
                app_logger.warning("crawled_content为空，跳过数据库更新")
            
        except Exception as db_error:
            app_logger.error(f"保存AI处理结果到数据库失败: {db_error}")
            # 不影响主流程，继续返回数据
        
        processing_time = time.time() - start_time
        
        return TLDRCrawlResponse(
            success=True,
            data=processed_data,
            cached=False,
            processing_time=processing_time
        )
        
    except Exception as e:
        app_logger.error(f"TLDR AI处理失败: {e}")
        return TLDRCrawlResponse(
            success=False,
            error=f"TLDR AI处理失败: {str(e)}",
            processing_time=time.time() - start_time
        )


@router.get("/database/content/{content_id}", response_model=DatabaseContentResponse)
async def get_crawled_content(content_id: int):
    """根据ID获取爬取内容"""
    try:
        content = db_manager.get_crawled_content_by_id(content_id)
        if content:
            return DatabaseContentResponse(
                success=True,
                data=content.to_dict()
            )
        else:
            return DatabaseContentResponse(
                success=False,
                error=f"未找到ID为 {content_id} 的内容"
            )
    except Exception as e:
        app_logger.error(f"获取爬取内容失败: {e}")
        return DatabaseContentResponse(
            success=False,
            error=f"获取内容失败: {str(e)}"
        )


@router.get("/database/content", response_model=DatabaseListResponse)
async def list_crawled_content(page: int = 1, limit: int = 20):
    """获取爬取内容列表"""
    try:
        if limit > 100:
            limit = 100  # 限制最大返回数量
        
        offset = (page - 1) * limit
        content_list = db_manager.list_crawled_content(limit=limit, offset=offset)
        
        # 转换为字典格式
        data = [content.to_dict() for content in content_list]
        
        return DatabaseListResponse(
            success=True,
            data=data,
            page=page,
            limit=limit,
            total=len(data)  # 简化版本，实际应该查询总数
        )
    except Exception as e:
        app_logger.error(f"获取爬取内容列表失败: {e}")
        return DatabaseListResponse(
            success=False,
            error=f"获取内容列表失败: {str(e)}"
        )


@router.get("/database/search", response_model=DatabaseListResponse)
async def search_crawled_content(q: str, limit: int = 20):
    """搜索爬取内容"""
    try:
        if limit > 100:
            limit = 100  # 限制最大返回数量
        
        content_list = db_manager.search_content(query=q, limit=limit)
        
        # 转换为字典格式
        data = [content.to_dict() for content in content_list]
        
        return DatabaseListResponse(
            success=True,
            data=data,
            total=len(data)
        )
    except Exception as e:
        app_logger.error(f"搜索爬取内容失败: {e}")
        return DatabaseListResponse(
            success=False,
            error=f"搜索内容失败: {str(e)}"
        )


@router.get("/database/stats", response_model=DatabaseStatsResponse)
async def get_crawl_stats():
    """获取爬取统计信息"""
    try:
        stats = db_manager.get_crawl_stats()
        return DatabaseStatsResponse(
            success=True,
            stats=stats.__dict__
        )
    except Exception as e:
        app_logger.error(f"获取爬取统计失败: {e}")
        return DatabaseStatsResponse(
            success=False,
            error=f"获取统计信息失败: {str(e)}"
        )


@router.get("/scheduler/markdown/{date}")
async def get_scheduler_markdown(date: str):
    """根据日期获取 chatgpt_scheduler 目录下的 Markdown 文件内容
    
    Args:
        date: 日期字符串，格式为 YYYY-MM-DD，例如 2025-10-07
    
    Returns:
        JSON 响应包含 Markdown 内容
    """
    import os
    from pathlib import Path
    
    try:
        # 构建文件路径
        base_dir = Path(__file__).parent.parent.parent  # 项目根目录
        md_file_path = base_dir / "data" / "chatgpt_scheduler" / f"{date}.md"
        
        app_logger.info(f"尝试读取 Markdown 文件: {md_file_path}")
        
        # 检查文件是否存在
        if not md_file_path.exists():
            app_logger.warning(f"Markdown 文件不存在: {md_file_path}")
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": f"找不到日期为 {date} 的 Markdown 文件",
                    "file_path": str(md_file_path)
                }
            )
        
        # 读取文件内容
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        app_logger.info(f"成功读取 Markdown 文件，长度: {len(content)}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "date": date,
                "content": content,
                "file_path": str(md_file_path)
            }
        )
        
    except Exception as e:
        app_logger.error(f"读取 Markdown 文件失败: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"读取文件失败: {str(e)}"
            }
        )