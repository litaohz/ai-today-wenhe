"""
数据库管理器
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path
import logging

from .models import CrawledContent, Article, CrawlStats

logger = logging.getLogger(__name__)


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = "data/crawled_content.db"):
        """初始化数据库管理器"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建爬取内容表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS crawled_content (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    subtitle TEXT,
                    content TEXT NOT NULL,
                    meta_description TEXT,
                    articles TEXT,  -- JSON格式存储文章列表
                    sections TEXT,  -- JSON格式存储章节列表
                    external_links TEXT,  -- JSON格式存储外部链接
                    crawled_at TEXT NOT NULL,
                    word_count INTEGER DEFAULT 0,
                    article_count INTEGER DEFAULT 0,
                    is_crawled BOOLEAN DEFAULT 0,  -- 是否完成爬取
                    is_ai_processed BOOLEAN DEFAULT 0,  -- 是否完成AI处理
                    processing_status TEXT DEFAULT 'pending',  -- pending, crawled, ai_processed, completed
                    summary TEXT,  -- AI生成的摘要
                    analysis TEXT,  -- AI生成的分析
                    keywords TEXT,  -- AI生成的关键词
                    `references` TEXT,  -- AI生成的参考文献
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建爬取统计表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS crawl_stats (
                    id INTEGER PRIMARY KEY,
                    total_crawls INTEGER DEFAULT 0,
                    successful_crawls INTEGER DEFAULT 0,
                    failed_crawls INTEGER DEFAULT 0,
                    total_articles INTEGER DEFAULT 0,
                    last_crawl_time TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 插入初始统计记录
            cursor.execute('''
                INSERT OR IGNORE INTO crawl_stats (id) VALUES (1)
            ''')
            
            # 添加新字段（如果不存在）
            try:
                cursor.execute('ALTER TABLE crawled_content ADD COLUMN is_crawled BOOLEAN DEFAULT 0')
            except sqlite3.OperationalError:
                pass  # 字段已存在
            
            try:
                cursor.execute('ALTER TABLE crawled_content ADD COLUMN is_ai_processed BOOLEAN DEFAULT 0')
            except sqlite3.OperationalError:
                pass  # 字段已存在
            
            try:
                cursor.execute('ALTER TABLE crawled_content ADD COLUMN processing_status TEXT DEFAULT "pending"')
            except sqlite3.OperationalError:
                pass  # 字段已存在
            
            # 添加AI处理结果字段
            try:
                cursor.execute('ALTER TABLE crawled_content ADD COLUMN summary TEXT')
            except sqlite3.OperationalError:
                pass  # 字段已存在
            
            try:
                cursor.execute('ALTER TABLE crawled_content ADD COLUMN analysis TEXT')
            except sqlite3.OperationalError:
                pass  # 字段已存在
            
            try:
                cursor.execute('ALTER TABLE crawled_content ADD COLUMN keywords TEXT')  # JSON格式存储关键词列表
            except sqlite3.OperationalError:
                pass  # 字段已存在
            
            try:
                cursor.execute('ALTER TABLE crawled_content ADD COLUMN `references` TEXT')  # JSON格式存储引用信息
            except sqlite3.OperationalError:
                pass  # 字段已存在
            
            # 更新现有记录的状态（如果有内容且articles不为空，说明已经AI处理过）
            cursor.execute('''
                UPDATE crawled_content 
                SET is_crawled = 1, 
                    is_ai_processed = CASE 
                        WHEN articles IS NOT NULL AND articles != '[]' AND articles != '' 
                        THEN 1 ELSE 0 
                    END,
                    processing_status = CASE 
                        WHEN articles IS NOT NULL AND articles != '[]' AND articles != '' 
                        THEN 'completed' ELSE 'crawled' 
                    END
                WHERE is_crawled IS NULL OR is_crawled = 0
            ''')
            
            # 创建索引
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_crawled_content_url 
                ON crawled_content(url)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_crawled_content_crawled_at 
                ON crawled_content(crawled_at)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_crawled_content_processing_status 
                ON crawled_content(processing_status)
            ''')
            
            conn.commit()
            logger.info(f"数据库初始化完成: {self.db_path}")
    
    def save_crawled_content(self, content: CrawledContent) -> int:
        """保存爬取的内容"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 准备数据
                data = content.to_dict()
                
                # 插入或更新内容
                cursor.execute('''
                    INSERT OR REPLACE INTO crawled_content 
                    (url, title, subtitle, content, meta_description, articles, 
                     sections, external_links, crawled_at, word_count, article_count,
                     is_crawled, is_ai_processed, processing_status, summary, analysis, keywords, `references`)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data['url'], data['title'], data['subtitle'], data['content'],
                    data['meta_description'], data['articles'], data['sections'],
                    data['external_links'], data['crawled_at'], 
                    data['word_count'], data['article_count'],
                    data.get('is_crawled', False), data.get('is_ai_processed', False), 
                    data.get('processing_status', 'pending'),
                    data.get('summary'), data.get('analysis'), data.get('keywords'),
                    data.get('references')
                ))
                
                content_id = cursor.lastrowid
                
                # 更新统计信息
                self._update_crawl_stats(cursor, success=True, article_count=len(content.articles))
                
                conn.commit()
                logger.info(f"成功保存爬取内容: {content.url}, ID: {content_id}")
                return content_id
                
        except Exception as e:
            logger.error(f"保存爬取内容失败: {e}")
            self._update_crawl_stats_failure()
            raise
    
    def get_crawled_content(self, url: str) -> Optional[CrawledContent]:
        """根据URL获取爬取内容"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM crawled_content WHERE url = ?
                ''', (url,))
                
                row = cursor.fetchone()
                if row:
                    data = dict(row)
                    return CrawledContent.from_dict(data)
                return None
                
        except Exception as e:
            logger.error(f"获取爬取内容失败: {e}")
            return None
    
    def update_processing_status(self, url: str, is_crawled: bool = None, 
                               is_ai_processed: bool = None, processing_status: str = None) -> bool:
        """更新处理状态"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 构建更新语句
                updates = []
                params = []
                
                if is_crawled is not None:
                    updates.append("is_crawled = ?")
                    params.append(is_crawled)
                
                if is_ai_processed is not None:
                    updates.append("is_ai_processed = ?")
                    params.append(is_ai_processed)
                
                if processing_status is not None:
                    updates.append("processing_status = ?")
                    params.append(processing_status)
                
                if not updates:
                    return True
                
                updates.append("updated_at = CURRENT_TIMESTAMP")
                params.append(url)
                
                cursor.execute(f'''
                    UPDATE crawled_content 
                    SET {", ".join(updates)}
                    WHERE url = ?
                ''', params)
                
                conn.commit()
                logger.info(f"更新处理状态成功: {url}")
                return True
                
        except Exception as e:
            logger.error(f"更新处理状态失败: {e}")
            return False
    
    def get_crawled_content_by_id(self, content_id: int) -> Optional[CrawledContent]:
        """根据ID获取爬取内容"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM crawled_content WHERE id = ?
                ''', (content_id,))
                
                row = cursor.fetchone()
                if row:
                    data = dict(row)
                    return CrawledContent.from_dict(data)
                return None
                
        except Exception as e:
            logger.error(f"获取爬取内容失败: {e}")
            return None
    
    def list_crawled_content(self, limit: int = 50, offset: int = 0) -> List[CrawledContent]:
        """获取爬取内容列表"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM crawled_content 
                    ORDER BY crawled_at DESC 
                    LIMIT ? OFFSET ?
                ''', (limit, offset))
                
                rows = cursor.fetchall()
                return [CrawledContent.from_dict(dict(row)) for row in rows]
                
        except Exception as e:
            logger.error(f"获取爬取内容列表失败: {e}")
            return []
    
    def search_content(self, query: str, limit: int = 20) -> List[CrawledContent]:
        """搜索内容"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM crawled_content 
                    WHERE title LIKE ? OR content LIKE ? OR subtitle LIKE ?
                    ORDER BY crawled_at DESC 
                    LIMIT ?
                ''', (f'%{query}%', f'%{query}%', f'%{query}%', limit))
                
                rows = cursor.fetchall()
                return [CrawledContent.from_dict(dict(row)) for row in rows]
                
        except Exception as e:
            logger.error(f"搜索内容失败: {e}")
            return []
    
    def get_crawl_stats(self) -> CrawlStats:
        """获取爬取统计信息"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM crawl_stats WHERE id = 1')
                row = cursor.fetchone()
                
                if row:
                    data = dict(row)
                    if data['last_crawl_time']:
                        data['last_crawl_time'] = datetime.fromisoformat(data['last_crawl_time'])
                    return CrawlStats(**data)
                else:
                    return CrawlStats()
                    
        except Exception as e:
            logger.error(f"获取爬取统计失败: {e}")
            return CrawlStats()
    
    def _update_crawl_stats(self, cursor, success: bool = True, article_count: int = 0):
        """更新爬取统计信息"""
        now = datetime.now().isoformat()
        
        if success:
            cursor.execute('''
                UPDATE crawl_stats SET 
                    total_crawls = total_crawls + 1,
                    successful_crawls = successful_crawls + 1,
                    total_articles = total_articles + ?,
                    last_crawl_time = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
            ''', (article_count, now))
        else:
            cursor.execute('''
                UPDATE crawl_stats SET 
                    total_crawls = total_crawls + 1,
                    failed_crawls = failed_crawls + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
            ''')
    
    def _update_crawl_stats_failure(self):
        """更新失败统计"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                self._update_crawl_stats(cursor, success=False)
                conn.commit()
        except Exception as e:
            logger.error(f"更新失败统计失败: {e}")
    
    def delete_crawled_content(self, content_id: int) -> bool:
        """删除爬取内容"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM crawled_content WHERE id = ?', (content_id,))
                conn.commit()
                
                if cursor.rowcount > 0:
                    logger.info(f"成功删除爬取内容: ID {content_id}")
                    return True
                else:
                    logger.warning(f"未找到要删除的内容: ID {content_id}")
                    return False
                    
        except Exception as e:
            logger.error(f"删除爬取内容失败: {e}")
            return False
    
    def close(self):
        """关闭数据库连接（SQLite自动管理连接，此方法为接口兼容性）"""
        pass