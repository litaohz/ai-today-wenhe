"""
缓存管理测试
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.utils.cache import CacheManager


class TestCacheManager:
    """CacheManager测试类"""
    
    @pytest.fixture
    def cache_manager(self):
        """创建缓存管理器实例"""
        return CacheManager()
    
    def test_cache_manager_initialization(self, cache_manager):
        """测试缓存管理器初始化"""
        assert cache_manager.redis_client is None
        assert cache_manager.prefix == "ai_today"
        assert cache_manager.default_ttl == 3600
    
    @pytest.mark.asyncio
    @patch('redis.asyncio.Redis')
    async def test_connect_success(self, mock_redis, cache_manager):
        """测试成功连接Redis"""
        mock_client = Mock()
        mock_client.ping = AsyncMock(return_value=True)
        mock_redis.return_value = mock_client
        
        result = await cache_manager.connect()
        
        assert result is True
        assert cache_manager.redis_client is not None
    
    @pytest.mark.asyncio
    @patch('redis.asyncio.Redis')
    async def test_connect_failure(self, mock_redis, cache_manager):
        """测试连接Redis失败"""
        mock_client = Mock()
        mock_client.ping = AsyncMock(side_effect=Exception("连接失败"))
        mock_redis.return_value = mock_client
        
        result = await cache_manager.connect()
        
        assert result is False
        assert cache_manager.redis_client is None
    
    @pytest.mark.asyncio
    async def test_disconnect(self, cache_manager):
        """测试断开连接"""
        # 模拟已连接状态
        mock_client = Mock()
        mock_client.close = AsyncMock()
        cache_manager.redis_client = mock_client
        
        await cache_manager.disconnect()
        
        mock_client.close.assert_called_once()
        assert cache_manager.redis_client is None
    
    def test_generate_key(self, cache_manager):
        """测试生成缓存键"""
        key = cache_manager._generate_key("test", "data")
        assert key == "ai_today:test:data"
        
        key = cache_manager._generate_key("user", "123", "profile")
        assert key == "ai_today:user:123:profile"
    
    @pytest.mark.asyncio
    async def test_get_without_redis(self, cache_manager):
        """测试没有Redis连接时的get操作"""
        result = await cache_manager.get("test_key")
        assert result is None
    
    @pytest.mark.asyncio
    async def test_set_without_redis(self, cache_manager):
        """测试没有Redis连接时的set操作"""
        result = await cache_manager.set("test_key", "test_value")
        assert result is False
    
    @pytest.mark.asyncio
    async def test_delete_without_redis(self, cache_manager):
        """测试没有Redis连接时的delete操作"""
        result = await cache_manager.delete("test_key")
        assert result is False
    
    @pytest.mark.asyncio
    async def test_get_with_redis_success(self, cache_manager):
        """测试有Redis连接时的成功get操作"""
        mock_client = Mock()
        mock_client.get = AsyncMock(return_value=b'{"test": "data"}')
        cache_manager.redis_client = mock_client
        
        result = await cache_manager.get("test_key")
        
        assert result == {"test": "data"}
        mock_client.get.assert_called_once_with("ai_today:test_key")
    
    @pytest.mark.asyncio
    async def test_get_with_redis_not_found(self, cache_manager):
        """测试Redis中找不到数据"""
        mock_client = Mock()
        mock_client.get = AsyncMock(return_value=None)
        cache_manager.redis_client = mock_client
        
        result = await cache_manager.get("test_key")
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_set_with_redis_success(self, cache_manager):
        """测试有Redis连接时的成功set操作"""
        mock_client = Mock()
        mock_client.setex = AsyncMock(return_value=True)
        cache_manager.redis_client = mock_client
        
        result = await cache_manager.set("test_key", {"test": "data"}, ttl=1800)
        
        assert result is True
        mock_client.setex.assert_called_once_with(
            "ai_today:test_key", 1800, '{"test": "data"}'
        )
    
    @pytest.mark.asyncio
    async def test_delete_with_redis_success(self, cache_manager):
        """测试有Redis连接时的成功delete操作"""
        mock_client = Mock()
        mock_client.delete = AsyncMock(return_value=1)
        cache_manager.redis_client = mock_client
        
        result = await cache_manager.delete("test_key")
        
        assert result is True
        mock_client.delete.assert_called_once_with("ai_today:test_key")
    
    @pytest.mark.asyncio
    async def test_get_crawl_cache(self, cache_manager):
        """测试获取爬取缓存"""
        mock_client = Mock()
        mock_client.get = AsyncMock(return_value=b'{"title": "test"}')
        cache_manager.redis_client = mock_client
        
        result = await cache_manager.get_crawl_cache("https://example.com")
        
        assert result == {"title": "test"}
        expected_key = "ai_today:crawl:https://example.com"
        mock_client.get.assert_called_once_with(expected_key)
    
    @pytest.mark.asyncio
    async def test_set_crawl_cache(self, cache_manager):
        """测试设置爬取缓存"""
        mock_client = Mock()
        mock_client.setex = AsyncMock(return_value=True)
        cache_manager.redis_client = mock_client
        
        data = {"title": "test", "content": "content"}
        result = await cache_manager.set_crawl_cache("https://example.com", data)
        
        assert result is True
        expected_key = "ai_today:crawl:https://example.com"
        mock_client.setex.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_ai_cache(self, cache_manager):
        """测试获取AI缓存"""
        mock_client = Mock()
        mock_client.get = AsyncMock(return_value=b'"test summary"')
        cache_manager.redis_client = mock_client
        
        result = await cache_manager.get_ai_cache("content", "summary")
        
        assert result == "test summary"
    
    @pytest.mark.asyncio
    async def test_set_ai_cache(self, cache_manager):
        """测试设置AI缓存"""
        mock_client = Mock()
        mock_client.setex = AsyncMock(return_value=True)
        cache_manager.redis_client = mock_client
        
        result = await cache_manager.set_ai_cache("content", "summary", "test summary")
        
        assert result is True
        mock_client.setex.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_json_serialization_error(self, cache_manager):
        """测试JSON序列化错误"""
        mock_client = Mock()
        mock_client.setex = AsyncMock(return_value=True)
        cache_manager.redis_client = mock_client
        
        # 尝试序列化不可序列化的对象
        class UnserializableObject:
            pass
        
        result = await cache_manager.set("test_key", UnserializableObject())
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_json_deserialization_error(self, cache_manager):
        """测试JSON反序列化错误"""
        mock_client = Mock()
        mock_client.get = AsyncMock(return_value=b'invalid json')
        cache_manager.redis_client = mock_client
        
        result = await cache_manager.get("test_key")
        
        assert result is None