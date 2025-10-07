"""
缓存模块
"""
import json
import hashlib
from typing import Any, Optional
import redis.asyncio as redis
from config import settings, app_logger


class CacheManager:
    """缓存管理器"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        
    async def connect(self):
        """连接Redis"""
        try:
            self.redis_client = redis.from_url(
                settings.cache.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            # 测试连接
            await self.redis_client.ping()
            app_logger.info("Redis连接成功")
        except Exception as e:
            app_logger.warning(f"Redis连接失败，将使用内存缓存: {e}")
            self.redis_client = None
            
    async def disconnect(self):
        """断开Redis连接"""
        if self.redis_client:
            await self.redis_client.close()
            
    def _generate_key(self, prefix: str, data: Any) -> str:
        """生成缓存键"""
        if isinstance(data, str):
            content = data
        else:
            content = json.dumps(data, sort_keys=True)
            
        hash_obj = hashlib.md5(content.encode('utf-8'))
        return f"{prefix}:{hash_obj.hexdigest()}"
        
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if not self.redis_client:
            return None
            
        try:
            value = await self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            app_logger.error(f"缓存获取失败 {key}: {e}")
            return None
            
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存"""
        if not self.redis_client:
            return False
            
        try:
            ttl = ttl or settings.cache.ttl
            serialized_value = json.dumps(value, ensure_ascii=False)
            await self.redis_client.setex(key, ttl, serialized_value)
            return True
        except Exception as e:
            app_logger.error(f"缓存设置失败 {key}: {e}")
            return False
            
    async def delete(self, key: str) -> bool:
        """删除缓存"""
        if not self.redis_client:
            return False
            
        try:
            await self.redis_client.delete(key)
            return True
        except Exception as e:
            app_logger.error(f"缓存删除失败 {key}: {e}")
            return False
            
    async def get_crawl_cache(self, url: str) -> Optional[dict]:
        """获取爬取缓存"""
        key = self._generate_key("crawl", url)
        return await self.get(key)
        
    async def set_crawl_cache(self, url: str, data: dict, ttl: Optional[int] = None) -> bool:
        """设置爬取缓存"""
        key = self._generate_key("crawl", url)
        return await self.set(key, data, ttl)
        
    async def get_ai_cache(self, content: str, operation: str) -> Optional[str]:
        """获取AI处理缓存"""
        cache_data = {"content": content, "operation": operation}
        key = self._generate_key("ai", cache_data)
        result = await self.get(key)
        return result.get("result") if result else None
        
    async def set_ai_cache(self, content: str, operation: str, result: str, ttl: Optional[int] = None) -> bool:
        """设置AI处理缓存"""
        cache_data = {"content": content, "operation": operation}
        key = self._generate_key("ai", cache_data)
        value = {"result": result, "operation": operation}
        return await self.set(key, value, ttl)


# 全局缓存实例
cache_manager = CacheManager()