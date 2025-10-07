"""
日志配置模块
"""
import os
import sys
from pathlib import Path
from loguru import logger
from .settings import settings


def setup_logging():
    """设置日志配置"""
    # 移除默认的日志处理器
    logger.remove()
    
    # 确保日志目录存在
    log_file_path = Path(settings.log.file)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 控制台日志
    logger.add(
        sys.stdout,
        format=settings.log.format,
        level=settings.log.level,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # 文件日志
    logger.add(
        settings.log.file,
        format=settings.log.format,
        level=settings.log.level,
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        backtrace=True,
        diagnose=True
    )
    
    logger.info("日志系统初始化完成")
    return logger


# 初始化日志
app_logger = setup_logging()