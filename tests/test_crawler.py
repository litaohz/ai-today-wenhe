"""
网页爬取模块测试
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from src.crawler.web_crawler import WebCrawler


class TestWebCrawler:
    """WebCrawler测试类"""
    
    @pytest.fixture
    def crawler(self):
        """创建爬虫实例"""
        return WebCrawler()
    
    @pytest.mark.asyncio
    async def test_crawler_initialization(self, crawler):
        """测试爬虫初始化"""
        assert crawler.session is None
        assert crawler.delay == 1.0
        assert crawler.max_retries == 3
        assert crawler.timeout == 30
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """测试上下文管理器"""
        async with WebCrawler() as crawler:
            assert crawler.session is not None
        # 退出后session应该被关闭
        assert crawler.session.closed
    
    @pytest.mark.asyncio
    async def test_robots_txt_check(self, crawler):
        """测试robots.txt检查"""
        async with crawler:
            # 测试允许的URL
            allowed = await crawler.can_fetch("https://example.com/page")
            assert isinstance(allowed, bool)
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.get')
    async def test_crawl_url_success(self, mock_get, crawler):
        """测试成功爬取URL"""
        # 模拟HTTP响应
        mock_response = Mock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="""
            <html>
                <head><title>Test Page</title></head>
                <body>
                    <h1>Test Article</h1>
                    <p>This is test content.</p>
                </body>
            </html>
        """)
        mock_response.headers = {'content-type': 'text/html'}
        mock_get.return_value.__aenter__.return_value = mock_response
        
        async with crawler:
            result = await crawler.crawl_url("https://example.com/test")
            
        assert result is not None
        assert result['title'] == 'Test Page'
        assert 'This is test content' in result['content']
        assert result['url'] == 'https://example.com/test'
        assert 'word_count' in result
        assert 'crawled_at' in result
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.get')
    async def test_crawl_url_failure(self, mock_get, crawler):
        """测试爬取失败"""
        # 模拟HTTP错误
        mock_get.side_effect = Exception("Network error")
        
        async with crawler:
            result = await crawler.crawl_url("https://example.com/test")
            
        assert result is None
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.get')
    async def test_crawl_tldr_ai(self, mock_get, crawler):
        """测试TLDR AI页面爬取"""
        # 模拟TLDR页面响应
        mock_response = Mock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="""
            <html>
                <head><title>TLDR AI - 2025-10-03</title></head>
                <body>
                    <article>
                        <h2>AI News Article 1</h2>
                        <p>Content of AI article 1</p>
                    </article>
                    <article>
                        <h2>AI News Article 2</h2>
                        <p>Content of AI article 2</p>
                    </article>
                </body>
            </html>
        """)
        mock_response.headers = {'content-type': 'text/html'}
        mock_get.return_value.__aenter__.return_value = mock_response
        
        async with crawler:
            result = await crawler.crawl_tldr_ai()
            
        assert result is not None
        assert 'TLDR AI' in result['title']
        assert 'AI News Article' in result['content']
    
    @pytest.mark.asyncio
    async def test_extract_content(self, crawler):
        """测试内容提取"""
        html = """
            <html>
                <head><title>Test Title</title></head>
                <body>
                    <h1>Main Heading</h1>
                    <p>First paragraph</p>
                    <p>Second paragraph</p>
                    <script>console.log('script');</script>
                    <style>body { color: red; }</style>
                </body>
            </html>
        """
        
        result = crawler.extract_content(html, "https://example.com")
        
        assert result['title'] == 'Test Title'
        assert 'Main Heading' in result['content']
        assert 'First paragraph' in result['content']
        assert 'Second paragraph' in result['content']
        assert 'script' not in result['content']  # 脚本应该被移除
        assert 'color: red' not in result['content']  # 样式应该被移除
        assert result['url'] == 'https://example.com'
        assert result['word_count'] > 0
    
    @pytest.mark.asyncio
    async def test_delay_between_requests(self, crawler):
        """测试请求间隔"""
        import time
        
        async with crawler:
            start_time = time.time()
            await crawler._delay()
            end_time = time.time()
            
            # 应该至少等待delay时间
            assert end_time - start_time >= crawler.delay - 0.1  # 允许小误差