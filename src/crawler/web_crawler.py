"""
网页爬取模块
支持robots.txt协议和请求间隔控制
"""
import asyncio
import time
from typing import Dict, List, Optional, Any
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
import aiohttp
from bs4 import BeautifulSoup
from config import settings, app_logger


class WebCrawler:
    """网页爬虫类"""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.last_request_time = 0.0
        self.robots_cache: Dict[str, RobotFileParser] = {}
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
        timeout = aiohttp.ClientTimeout(total=settings.crawler.timeout)
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': settings.crawler.user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
            
    def _get_robots_parser(self, base_url: str) -> Optional[RobotFileParser]:
        """获取robots.txt解析器"""
        if not settings.crawler.respect_robots_txt:
            return None
            
        if base_url in self.robots_cache:
            return self.robots_cache[base_url]
            
        try:
            robots_url = urljoin(base_url, '/robots.txt')
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            self.robots_cache[base_url] = rp
            app_logger.info(f"已加载robots.txt: {robots_url}")
            return rp
        except Exception as e:
            app_logger.warning(f"无法加载robots.txt {base_url}: {e}")
            return None
            
    def _can_fetch(self, url: str) -> bool:
        """检查是否可以爬取URL"""
        if not settings.crawler.respect_robots_txt:
            return True
            
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        robots_parser = self._get_robots_parser(base_url)
        if robots_parser is None:
            return True
            
        return robots_parser.can_fetch(settings.crawler.user_agent, url)
        
    async def _fetch_with_retry(self, url: str) -> Optional[str]:
        """带重试机制的网页获取"""
        if not self._can_fetch(url):
            app_logger.warning(f"robots.txt禁止访问: {url}")
            return None
            
        for attempt in range(settings.crawler.max_retries):
            try:
                # 实现简单的速率限制
                current_time = time.time()
                time_since_last = current_time - self.last_request_time
                if time_since_last < settings.crawler.request_delay:
                    await asyncio.sleep(settings.crawler.request_delay - time_since_last)
                
                self.last_request_time = time.time()
                app_logger.info(f"正在爬取 (尝试 {attempt + 1}/{settings.crawler.max_retries}): {url}")
                
                async with self.session.get(url) as response:
                        if response.status == 200:
                            content = await response.text()
                            app_logger.info(f"成功爬取: {url} (状态码: {response.status})")
                            return content
                        else:
                            app_logger.warning(f"HTTP错误: {url} (状态码: {response.status})")
                            
            except asyncio.TimeoutError:
                app_logger.warning(f"请求超时: {url} (尝试 {attempt + 1})")
            except Exception as e:
                app_logger.error(f"爬取失败: {url} (尝试 {attempt + 1}): {e}")
                
            if attempt < settings.crawler.max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避
                
        app_logger.error(f"所有重试失败: {url}")
        return None
        
    def _extract_content(self, html: str, url: str) -> Dict[str, Any]:
        """提取网页内容"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 移除脚本和样式标签
            for script in soup(["script", "style"]):
                script.decompose()
                
            # 提取标题
            title = ""
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text().strip()
                
            # 针对TLDR AI网站的特殊处理
            if 'tldr.tech' in url:
                return self._extract_tldr_content(soup, url, title)
            
            # 通用内容提取逻辑
            return self._extract_generic_content(soup, url, title)
            
        except Exception as e:
            app_logger.error(f"内容提取失败 {url}: {e}")
            return {
                'url': url,
                'title': '',
                'content': '',
                'meta_description': '',
                'links': [],
                'articles': [],
                'sections': [],
                'word_count': 0,
                'crawled_at': time.time(),
                'error': str(e)
            }
    
    def _extract_tldr_content(self, soup: BeautifulSoup, url: str, title: str) -> Dict[str, Any]:
        """专门提取TLDR AI网站内容，包含内容过滤和去重"""
        # 提取主标题
        main_title = title
        h1_tag = soup.find('h1')
        if h1_tag:
            main_title = h1_tag.get_text().strip()
        
        # 提取副标题
        subtitle = ""
        h2_tag = soup.find('h2')
        if h2_tag:
            subtitle = h2_tag.get_text().strip()
        
        # 提取所有文章 - 改进版本，从外部链接中提取文章
        articles = []
        seen_links = set()  # 用于去重链接
        
        # 首先提取传统的article元素
        article_elements = soup.find_all('article')
        for article in article_elements:
            # 提取文章标题
            article_title = ""
            title_elem = article.find(['h3', 'h4', 'h5'])
            if title_elem:
                article_title = title_elem.get_text().strip()
            
            # 提取文章内容
            article_content = ""
            # 移除标题后获取剩余文本
            import copy
            article_copy = copy.copy(article)
            for heading in article_copy.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                heading.decompose()
            article_content = article_copy.get_text(separator=' ', strip=True)
            
            # 过滤赞助内容
            if self._is_sponsored_content(article_title, article_content):
                continue
            
            # 计算字数
            word_count = len(article_content.split()) if article_content else 0
            
            # 提取文章链接并去重
            article_links = []
            for link in article.find_all('a', href=True):
                href = link['href']
                link_text = link.get_text().strip()
                if href and link_text and not href.startswith('#'):
                    absolute_url = urljoin(url, href)
                    
                    # 清理URL参数用于去重
                    clean_url = self._clean_url_for_dedup(absolute_url)
                    
                    if clean_url not in seen_links:
                        seen_links.add(clean_url)
                        article_links.append({
                            'url': absolute_url,
                            'text': link_text
                        })
            
            if article_title or article_content:
                articles.append({
                    'title': article_title,
                    'content': article_content,
                    'links': article_links,
                    'word_count': word_count
                })
        
        # 从外部链接中提取文章（TLDR AI的主要内容）
        app_logger.info(f"开始从外部链接中提取文章，当前已有 {len(articles)} 篇文章")
        external_article_count = 0
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            link_text = link.get_text().strip()
            
            # 检查是否包含阅读时间
            has_reading_time = ('minute read' in link_text or 'hour read' in link_text)
            
            # 只处理外部链接且包含阅读时间的文章
            if (href and link_text and 
                href.startswith('http') and 
                'tldr.tech' not in href and
                not href.startswith('#') and
                has_reading_time):
                
                app_logger.info(f"找到候选文章: {link_text[:50]}...")
                
                # 过滤赞助内容
                if self._is_sponsored_content(link_text, ""):
                    app_logger.info(f"过滤赞助内容: {link_text[:50]}...")
                    continue
                
                absolute_url = urljoin(url, href)
                clean_url = self._clean_url_for_dedup(absolute_url)
                
                if clean_url not in seen_links:
                    seen_links.add(clean_url)
                    
                    # 提取阅读时间
                    import re
                    time_match = re.search(r'\((\d+)\s+(minute|hour)\s+read\)', link_text)
                    reading_time = time_match.group(0) if time_match else ""
                    
                    # 清理标题（移除阅读时间）
                    clean_title = re.sub(r'\s*\(\d+\s+(minute|hour)\s+read\)\s*$', '', link_text).strip()
                    
                    articles.append({
                        'title': clean_title,
                        'content': f"External article: {clean_title} {reading_time}",
                        'links': [{
                            'url': absolute_url,
                            'text': link_text
                        }],
                        'word_count': len(clean_title.split()) + 3,  # 估算字数
                        'reading_time': reading_time,
                        'source_url': absolute_url
                    })
                    external_article_count += 1
                    app_logger.info(f"成功添加文章: {clean_title}")
                else:
                    app_logger.info(f"链接已存在，跳过: {clean_url}")
        
        app_logger.info(f"从外部链接中提取了 {external_article_count} 篇文章，总计 {len(articles)} 篇文章")
        
        # 提取指定的章节
        sections = []
        target_section_titles = [
            "Headlines & Launches",
            "Deep Dives & Analysis", 
            "Engineering & Research",
            "Miscellaneous",
            "Quick Links"
        ]
        
        # 查找所有section元素
        section_elements = soup.find_all('section')
        app_logger.info(f"找到 {len(section_elements)} 个section元素")
        
        for section_elem in section_elements:
            # 查找section的标题
            section_title = ""
            
            # 尝试多种方式查找标题
            header = section_elem.find('header')
            if header:
                h3 = header.find('h3')
                if h3:
                    section_title = h3.get_text(strip=True)
            
            if not section_title:
                h3 = section_elem.find('h3')
                if h3:
                    section_title = h3.get_text(strip=True)
            
            # 只处理目标sections
            if section_title in target_section_titles:
                app_logger.info(f"找到目标section: {section_title}")
                
                section_articles = []
                
                # 查找该section下的所有article元素
                article_elements = section_elem.find_all('article')
                app_logger.info(f"  section '{section_title}' 包含 {len(article_elements)} 个article元素")
                
                for article_elem in article_elements:
                    # 提取文章的实际内容
                    content_div = article_elem.find('div', class_='newsletter-html')
                    article_content = ""
                    if content_div:
                        article_content = content_div.get_text(strip=True)
                    
                    # 查找article中的链接
                    links = article_elem.find_all('a', href=True)
                    
                    for link in links:
                        href = link.get('href', '')
                        link_text = link.get_text(strip=True)
                        
                        if href and link_text:
                            # 处理相对链接
                            if href.startswith('/'):
                                absolute_url = f"https://tldr.tech{href}"
                            elif href.startswith('http'):
                                absolute_url = href
                            else:
                                continue
                            
                            # 提取阅读时间
                            import re
                            time_match = re.search(r'\((\d+)\s+(minute|hour)\s+read\)', link_text)
                            reading_time = time_match.group(0) if time_match else ""
                            
                            # 清理标题（移除阅读时间）
                            clean_title = re.sub(r'\s*\(\d+\s+(minute|hour)\s+read\)\s*$', '', link_text).strip()
                            
                            # 计算实际的word count
                            word_count = len(article_content.split()) if article_content else len(clean_title.split())
                            
                            section_articles.append({
                                'title': clean_title,
                                'content': article_content or f"No content available for: {clean_title}",
                                'links': [{
                                    'url': absolute_url,
                                    'text': link_text
                                }],
                                'word_count': word_count,
                                'reading_time': reading_time,
                                'source_url': absolute_url
                            })
                
                sections.append({
                    'title': section_title,
                    'articles': section_articles,
                    'article_count': len(section_articles)
                })
                
                app_logger.info(f"  section '{section_title}' 添加了 {len(section_articles)} 篇文章")
        
        app_logger.info(f"总共提取了 {len(sections)} 个目标sections")
        
        # 提取真正的外部链接（非TLDR内部链接，非section文章链接）
        external_links = []
        
        # 收集所有section中已经处理的链接URL，避免重复
        section_urls = set()
        for section in sections:
            for article in section['articles']:
                for link in article['links']:
                    section_urls.add(link['url'])
        
        # 查找页面中的其他外部链接
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            link_text = link.get_text(strip=True)
            
            # 处理链接URL
            if href.startswith('/'):
                absolute_url = f"https://tldr.tech{href}"
            elif href.startswith('http'):
                absolute_url = href
            else:
                continue
            
            # 过滤条件：真正的外部链接
            if (href and link_text and 
                not href.startswith('#') and           # 排除锚点链接
                'tldr.tech' not in absolute_url and    # 排除TLDR内部链接
                absolute_url not in section_urls and   # 排除已在sections中的链接
                len(link_text) > 5 and                 # 排除过短的链接文本
                not link_text.lower().startswith('unsubscribe') and  # 排除退订链接
                not link_text.lower().startswith('manage')):         # 排除管理链接
                
                external_links.append({
                    'url': absolute_url,
                    'text': link_text
                })
        
        app_logger.info(f"提取了 {len(external_links)} 个真正的外部链接（排除了sections中的 {len(section_urls)} 个链接）")
        
        # 生成完整内容文本
        full_content_parts = [main_title]
        if subtitle:
            full_content_parts.append(subtitle)
        
        for article in articles:
            if article['title']:
                full_content_parts.append(f"\n{article['title']}")
            if article['content']:
                full_content_parts.append(article['content'])
        
        full_content = '\n'.join(full_content_parts)
        
        # 提取元数据
        meta_description = ""
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag:
            meta_description = meta_tag.get('content', '').strip()
        
        return {
            'url': url,
            'title': main_title,
            'subtitle': subtitle,
            'content': full_content,
            'meta_description': meta_description,
            'articles': articles,
            'sections': sections,
            'external_links': external_links,
            'links': external_links,  # 保持向后兼容
            'article_count': len(articles),
            'external_link_count': len(external_links),
            'word_count': len(full_content.split()),
            'crawled_at': time.time(),
            'filtered_stats': {
                'total_unique_links': len(seen_links),
                'filtered_articles': len(article_elements) - len(articles)
            }
        }
    
    def _is_sponsored_content(self, title: str, content: str) -> bool:
        """检测是否为赞助内容"""
        import re
        
        # 使用单词边界匹配，避免误判
        sponsored_keywords = [
            r'\bsponsor\b', r'\bsponsored\b', r'\badvertisement\b', 
            r'\bpromo\b', r'\bpromotion\b', r'\bfree trial\b', 
            r'\bget started\b', r'\bsign up\b', r'\bregister now\b'
        ]
        
        text_to_check = (title + ' ' + content).lower()
        
        # 检查是否包含赞助关键词（使用正则表达式单词边界）
        for pattern in sponsored_keywords:
            if re.search(pattern, text_to_check):
                return True
        
        # 检查是否有过多的营销语言
        marketing_phrases = [
            'save 50%', 'free credits', 'limited time', 'act now',
            'don\'t miss', 'exclusive offer', 'special deal'
        ]
        
        marketing_count = sum(1 for phrase in marketing_phrases if phrase in text_to_check)
        if marketing_count >= 2:  # 如果包含2个或以上营销短语，认为是广告
            return True
        
        return False
    
    def _clean_url_for_dedup(self, url: str) -> str:
        """清理URL用于去重，移除UTM参数等"""
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
        
        parsed = urlparse(url)
        
        # 移除常见的跟踪参数
        tracking_params = {
            'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
            'ref', 'source', 'campaign', 'medium', 'content'
        }
        
        if parsed.query:
            query_params = parse_qs(parsed.query)
            # 过滤掉跟踪参数
            filtered_params = {k: v for k, v in query_params.items() 
                             if k not in tracking_params}
            
            # 重新构建查询字符串
            new_query = urlencode(filtered_params, doseq=True) if filtered_params else ''
            
            # 重新构建URL
            clean_parsed = parsed._replace(query=new_query)
            return urlunparse(clean_parsed)
        
        return url
    
    def _extract_generic_content(self, soup: BeautifulSoup, url: str, title: str) -> Dict[str, Any]:
        """通用内容提取逻辑"""
        # 提取主要内容
        content_selectors = [
            'article',
            '.content',
            '.post-content',
            '.entry-content',
            'main',
            '#content',
            '.main-content'
        ]
        
        main_content = ""
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                main_content = content_elem.get_text(separator='\n', strip=True)
                break
                
        # 如果没有找到主要内容区域，使用body
        if not main_content:
            body = soup.find('body')
            if body:
                main_content = body.get_text(separator='\n', strip=True)
                
        # 提取所有链接
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            link_text = link.get_text().strip()
            if href and link_text:
                absolute_url = urljoin(url, href)
                links.append({
                    'url': absolute_url,
                    'text': link_text
                })
                
        # 提取元数据
        meta_description = ""
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag:
            meta_description = meta_tag.get('content', '').strip()
            
        return {
            'url': url,
            'title': title,
            'content': main_content,
            'meta_description': meta_description,
            'links': links,
            'articles': [],
            'sections': [],
            'word_count': len(main_content.split()),
            'crawled_at': time.time()
        }
            
    async def crawl_url(self, url: str) -> Optional[Dict[str, Any]]:
        """爬取单个URL"""
        html = await self._fetch_with_retry(url)
        if html is None:
            return None
            
        return self._extract_content(html, url)
        
    async def crawl_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """批量爬取URL"""
        tasks = [self.crawl_url(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        crawled_data = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                app_logger.error(f"爬取异常 {urls[i]}: {result}")
            elif result is not None:
                crawled_data.append(result)
                
        return crawled_data
        
    async def crawl_tldr_ai(self, url: str = None) -> Optional[Dict[str, Any]]:
        """爬取TLDR AI页面"""
        target_url = url if url else settings.crawler.target_url
        return await self.crawl_url(target_url)