"""
主应用程序入口
"""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api import router
from src.utils import cache_manager
from config import settings, app_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用程序生命周期管理"""
    # 启动时
    app_logger.info("启动AI Today自动化系统...")
    
    try:
        # 连接Redis缓存
        await cache_manager.connect()
        app_logger.info("Redis缓存连接成功")
    except Exception as e:
        app_logger.warning(f"Redis缓存连接失败: {e}")
    
    app_logger.info("系统启动完成")
    
    yield
    
    # 关闭时
    app_logger.info("正在关闭系统...")
    
    try:
        # 断开Redis连接
        await cache_manager.disconnect()
        app_logger.info("Redis缓存连接已断开")
    except Exception as e:
        app_logger.warning(f"Redis缓存断开失败: {e}")
    
    app_logger.info("系统已关闭")


# 创建FastAPI应用
app = FastAPI(
    title="AI Today 自动化系统",
    description="基于Azure OpenAI的网页爬取和内容分析系统",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI Today 自动化系统",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP异常处理器"""
    app_logger.error(f"HTTP异常: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """通用异常处理器"""
    app_logger.error(f"未处理的异常: {type(exc).__name__} - {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "内部服务器错误", "status_code": 500}
    )


if __name__ == "__main__":
    import uvicorn
    
    # 运行服务器
    uvicorn.run(
        "main:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.api.debug,
        log_level="info"
    )