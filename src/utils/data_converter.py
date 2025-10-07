"""
数据转换工具类
用于处理爬虫数据到数据库模型对象的转换
"""
from datetime import datetime
from typing import Dict, List, Any, Optional

from src.database.models import CrawledContent, Article, Section


class DataConverter:
    """数据转换工具类"""
    
    @staticmethod
    def convert_article_dict_to_model(article_dict: Dict[str, Any]) -> Article:
        """
        将文章字典转换为 Article 模型对象
        
        Args:
            article_dict: 文章数据字典
            
        Returns:
            Article: Article 模型对象
        """
        return Article(
            title=article_dict.get('title', ''),
            content=article_dict.get('content', ''),
            links=article_dict.get('links', []),
            word_count=article_dict.get('word_count', 0),
            reading_time=article_dict.get('reading_time')
        )
    
    @staticmethod
    def convert_articles_list_to_models(articles_data: List[Dict[str, Any]]) -> List[Article]:
        """
        将文章字典列表转换为 Article 模型对象列表
        
        Args:
            articles_data: 文章数据字典列表
            
        Returns:
            List[Article]: Article 模型对象列表
        """
        articles = []
        for article_dict in articles_data:
            article = DataConverter.convert_article_dict_to_model(article_dict)
            articles.append(article)
        return articles
    
    @staticmethod
    def convert_section_dict_to_model(section_dict: Dict[str, Any]) -> Section:
        """
        将分区字典转换为 Section 模型对象
        
        Args:
            section_dict: 分区数据字典
            
        Returns:
            Section: Section 模型对象
        """
        # 转换 section 中的 articles
        section_articles = DataConverter.convert_articles_list_to_models(
            section_dict.get('articles', [])
        )
        
        return Section(
            title=section_dict.get('title', ''),
            articles=section_articles,
            article_count=section_dict.get('article_count', len(section_articles))
        )
    
    @staticmethod
    def convert_sections_list_to_models(sections_data: List[Dict[str, Any]]) -> List[Section]:
        """
        将分区字典列表转换为 Section 模型对象列表
        
        Args:
            sections_data: 分区数据字典列表
            
        Returns:
            List[Section]: Section 模型对象列表
        """
        sections = []
        for section_dict in sections_data:
            section = DataConverter.convert_section_dict_to_model(section_dict)
            sections.append(section)
        return sections
    
    @staticmethod
    def convert_crawled_data_to_model(
        article_data: Dict[str, Any], 
        target_url: str,
        processing_status: str = 'crawled'
    ) -> CrawledContent:
        """
        将爬虫数据转换为 CrawledContent 模型对象
        
        Args:
            article_data: 爬虫返回的文章数据
            target_url: 目标URL
            processing_status: 处理状态，默认为 'crawled'
            
        Returns:
            CrawledContent: CrawledContent 模型对象
        """
        # 转换 articles 数据
        articles = DataConverter.convert_articles_list_to_models(
            article_data.get('articles', [])
        )
        
        # 转换 sections 数据
        sections = DataConverter.convert_sections_list_to_models(
            article_data.get('sections', [])
        )
        
        # 创建 CrawledContent 对象
        return CrawledContent(
            url=target_url,
            title=article_data.get('title', ''),
            subtitle=article_data.get('subtitle', ''),
            content=article_data.get('content', ''),
            meta_description=article_data.get('meta_description', ''),
            articles=articles,
            sections=sections,
            external_links=article_data.get('external_links', []),
            crawled_at=datetime.now(),
            is_crawled=True,
            is_ai_processed=processing_status == 'ai_processed',
            processing_status=processing_status
        )
    
    @staticmethod
    def update_with_ai_results(
        crawled_content: CrawledContent,
        ai_result: Dict[str, Any]
    ) -> CrawledContent:
        """
        使用AI处理结果更新 CrawledContent 对象
        
        Args:
            crawled_content: 原始的 CrawledContent 对象
            ai_result: AI处理结果
            
        Returns:
            CrawledContent: 更新后的 CrawledContent 对象
        """
        # 更新AI处理相关字段
        crawled_content.summary = ai_result.get('summary', '')
        crawled_content.analysis = ai_result.get('analysis', '')
        crawled_content.keywords = ai_result.get('keywords', [])
        crawled_content.references = ai_result.get('references', [])
        crawled_content.is_ai_processed = True
        crawled_content.processing_status = 'completed'
        
        return crawled_content