"""
API端点测试
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from main import app


class TestAPI:
    """API测试类"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """测试根端点"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"
    
    def test_health_check(self, client):
        """测试健康检查端点"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "services" in data
        assert "version" in data
    
    @patch('src.crawler.WebCrawler.crawl_url')
    def test_crawl_endpoint_success(self, mock_crawl, client):
        """测试爬取端点成功"""
        # 模拟爬取结果
        mock_crawl.return_value = {
            'title': '测试文章',
            'content': '这是测试内容',
            'url': 'https://example.com',
            'word_count': 10,
            'crawled_at': 1234567890
        }
        
        response = client.post(
            "/api/v1/crawl",
            json={"url": "https://example.com", "use_cache": False}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["title"] == "测试文章"
    
    @patch('src.crawler.WebCrawler.crawl_url')
    def test_crawl_endpoint_failure(self, mock_crawl, client):
        """测试爬取端点失败"""
        mock_crawl.return_value = None
        
        response = client.post(
            "/api/v1/crawl",
            json={"url": "https://example.com", "use_cache": False}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "error" in data
    
    @patch('src.ai.AzureOpenAIClient.generate_summary')
    def test_summary_endpoint_success(self, mock_summary, client):
        """测试摘要端点成功"""
        mock_summary.return_value = "这是一个测试摘要"
        
        response = client.post(
            "/api/v1/summary",
            json={
                "content": "测试内容",
                "title": "测试标题",
                "use_cache": False
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["summary"] == "这是一个测试摘要"
    
    @patch('src.ai.AzureOpenAIClient.generate_summary')
    def test_summary_endpoint_failure(self, mock_summary, client):
        """测试摘要端点失败"""
        mock_summary.return_value = None
        
        response = client.post(
            "/api/v1/summary",
            json={
                "content": "测试内容",
                "title": "测试标题",
                "use_cache": False
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "error" in data
    
    @patch('src.ai.AzureOpenAIClient.generate_analysis')
    def test_analysis_endpoint_success(self, mock_analysis, client):
        """测试分析端点成功"""
        mock_analysis.return_value = "这是一个深度分析"
        
        response = client.post(
            "/api/v1/analysis",
            json={
                "content": "测试内容",
                "title": "测试标题",
                "use_cache": False
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["analysis"] == "这是一个深度分析"
    
    @patch('src.ai.AzureOpenAIClient.generate_keywords')
    def test_keywords_endpoint_success(self, mock_keywords, client):
        """测试关键词端点成功"""
        mock_keywords.return_value = ["关键词1", "关键词2", "关键词3"]
        
        response = client.post(
            "/api/v1/keywords",
            json={
                "content": "测试内容",
                "title": "测试标题",
                "use_cache": False
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["keywords"] == ["关键词1", "关键词2", "关键词3"]
    
    @patch('src.ai.AzureOpenAIClient.process_article')
    @patch('src.crawler.WebCrawler.crawl_url')
    def test_process_endpoint_success(self, mock_crawl, mock_process, client):
        """测试文章处理端点成功"""
        # 模拟爬取结果
        mock_crawl.return_value = {
            'title': '测试文章',
            'content': '这是测试内容',
            'url': 'https://example.com',
            'word_count': 10,
            'crawled_at': 1234567890
        }
        
        # 模拟AI处理结果
        mock_process.return_value = {
            'original_data': mock_crawl.return_value,
            'summary': '测试摘要',
            'analysis': '测试分析',
            'keywords': ['关键词1', '关键词2'],
            'processing_time': 1.5,
            'processed_at': 1234567890
        }
        
        response = client.post(
            "/api/v1/process",
            json={
                "url": "https://example.com",
                "use_cache": False
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["summary"] == "测试摘要"
    
    @patch('src.ai.AzureOpenAIClient.process_article')
    @patch('src.crawler.WebCrawler.crawl_tldr_ai')
    def test_tldr_endpoint_success(self, mock_crawl_tldr, mock_process, client):
        """测试TLDR端点成功"""
        # 模拟TLDR爬取结果
        mock_crawl_tldr.return_value = {
            'title': 'TLDR AI - 2025-10-03',
            'content': 'AI新闻内容',
            'url': 'https://tldr.tech/ai/2025-10-03',
            'word_count': 100,
            'crawled_at': 1234567890
        }
        
        # 模拟AI处理结果
        mock_process.return_value = {
            'original_data': mock_crawl_tldr.return_value,
            'summary': 'TLDR摘要',
            'analysis': 'TLDR分析',
            'keywords': ['AI', '新闻'],
            'processing_time': 2.0,
            'processed_at': 1234567890
        }
        
        response = client.get("/api/v1/tldr")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["summary"] == "TLDR摘要"
    
    def test_invalid_request_data(self, client):
        """测试无效请求数据"""
        # 测试缺少必需字段
        response = client.post("/api/v1/crawl", json={})
        assert response.status_code == 422  # Validation error
        
        # 测试无效URL格式
        response = client.post(
            "/api/v1/crawl",
            json={"url": "invalid-url", "use_cache": False}
        )
        assert response.status_code == 422
    
    def test_cors_headers(self, client):
        """测试CORS头"""
        response = client.options("/api/v1/health")
        # FastAPI的TestClient可能不会完全模拟CORS，但我们可以检查基本响应
        assert response.status_code in [200, 405]  # OPTIONS可能不被支持，但不应该是500错误