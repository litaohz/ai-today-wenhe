"""
配置管理模块
"""
import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Settings(BaseSettings):
    """主配置类"""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # Azure OpenAI配置
    azure_openai_endpoint: str = Field(
        default="https://ai-taoli1msai163197739760.cognitiveservices.azure.com/",
        env="AZURE_OPENAI_ENDPOINT"
    )
    azure_openai_api_key: str = Field(default="", env="AZURE_OPENAI_API_KEY")
    azure_openai_api_version: str = Field(default="2024-12-01-preview", env="AZURE_OPENAI_API_VERSION")
    azure_openai_model_name: str = Field(default="gpt-5", env="AZURE_OPENAI_MODEL_NAME")
    azure_openai_deployment: str = Field(default="gpt-5", env="AZURE_OPENAI_DEPLOYMENT")
    azure_openai_max_tokens: int = Field(default=16384, env="AZURE_OPENAI_MAX_TOKENS")
    
    # 爬虫配置
    crawler_user_agent: str = Field(default="AI-Today-Bot/1.0", env="CRAWLER_USER_AGENT")
    crawler_request_delay: float = Field(default=1.0, env="CRAWLER_REQUEST_DELAY")
    crawler_respect_robots_txt: bool = Field(default=True, env="CRAWLER_RESPECT_ROBOTS_TXT")
    crawler_max_retries: int = Field(default=3, env="CRAWLER_MAX_RETRIES")
    crawler_timeout: int = Field(default=30, env="CRAWLER_TIMEOUT")
    crawler_target_url: str = Field(
        default="https://tldr.tech/ai/2025-10-03",
        env="CRAWLER_TARGET_URL"
    )
    
    # 缓存配置
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")
    
    # API配置
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_debug: bool = Field(default=False, env="API_DEBUG")
    api_title: str = "AI Today 自动化系统"
    api_description: str = "网页爬取、内容处理和AI摘要生成系统"
    api_version: str = "1.0.0"
    
    # 日志配置
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/app.log", env="LOG_FILE")
    log_format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"


class AzureOpenAISettings:
    """Azure OpenAI配置包装器"""
    def __init__(self, settings: Settings):
        self.endpoint = settings.azure_openai_endpoint
        self.api_key = settings.azure_openai_api_key
        self.api_version = settings.azure_openai_api_version
        self.model_name = settings.azure_openai_model_name
        self.deployment = settings.azure_openai_deployment
        self.max_tokens = settings.azure_openai_max_tokens


class CrawlerSettings:
    """爬虫配置包装器"""
    def __init__(self, settings: Settings):
        self.user_agent = settings.crawler_user_agent
        self.request_delay = settings.crawler_request_delay
        self.respect_robots_txt = settings.crawler_respect_robots_txt
        self.max_retries = settings.crawler_max_retries
        self.timeout = settings.crawler_timeout
        self.target_url = settings.crawler_target_url


class CacheSettings:
    """缓存配置包装器"""
    def __init__(self, settings: Settings):
        self.redis_url = settings.redis_url
        self.ttl = settings.cache_ttl


class APISettings:
    """API配置包装器"""
    def __init__(self, settings: Settings):
        self.host = settings.api_host
        self.port = settings.api_port
        self.debug = settings.api_debug
        self.title = settings.api_title
        self.description = settings.api_description
        self.version = settings.api_version


class LogSettings:
    """日志配置包装器"""
    def __init__(self, settings: Settings):
        self.level = settings.log_level
        self.file = settings.log_file
        self.format = settings.log_format


# 创建全局配置实例
_settings = Settings()

# 创建配置包装器
class ConfigWrapper:
    def __init__(self):
        self.azure_openai = AzureOpenAISettings(_settings)
        self.crawler = CrawlerSettings(_settings)
        self.cache = CacheSettings(_settings)
        self.api = APISettings(_settings)
        self.log = LogSettings(_settings)

# 全局配置实例
settings = ConfigWrapper()