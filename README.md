# AI Today 自动化系统

基于Azure OpenAI的网页爬取和内容分析系统，专门用于处理TLDR AI新闻内容。

## 功能特性

- 🕷️ **智能网页爬取**: 支持robots.txt协议，智能请求间隔控制
- 🤖 **AI内容分析**: 集成Azure OpenAI GPT-5进行文章摘要、深度分析和关键词提取
- ⚡ **高性能后端**: 基于FastAPI和uvicorn的异步处理架构
- 💾 **智能缓存**: Redis缓存机制，提升响应速度
- 📊 **完整API**: RESTful API接口，支持多种内容处理需求
- 🔧 **模块化设计**: 易于维护和扩展的代码架构

## 系统架构

```
├── config/              # 配置管理
│   ├── settings.py      # 环境配置
│   └── logging.py       # 日志配置
├── src/
│   ├── crawler/         # 网页爬取模块
│   ├── ai/             # Azure OpenAI集成
│   ├── api/            # FastAPI路由和模型
│   └── utils/          # 工具类（缓存等）
├── tests/              # 测试用例
├── logs/               # 日志文件
└── main.py             # 应用入口
```

## 快速开始

### 1. 环境准备

确保已安装Python 3.8+和uv包管理器：

```bash
# 安装uv（如果尚未安装）
pip install uv
```

### 2. 安装依赖

```bash
# 使用uv安装依赖
uv sync
```

### 3. 环境配置

复制环境变量模板并配置：

```bash
cp .env.example .env
```

编辑`.env`文件，配置以下关键参数：

```env
# Azure OpenAI配置
AZURE_OPENAI_ENDPOINT=https://ai-taoli1msai163197739760.cognitiveservices.azure.com/
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_MODEL_NAME=gpt-5
AZURE_OPENAI_DEPLOYMENT=gpt-5

# 爬取目标
CRAWLER_TARGET_URL=https://tldr.tech/ai/2025-10-03

# Redis缓存（可选）
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 4. 启动服务

```bash
# 使用uv运行
uv run python main.py

# 或者直接使用uvicorn
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

服务启动后，访问：
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/api/v1/health

## API使用指南

### 1. 健康检查

```bash
curl http://localhost:8000/api/v1/health
```

### 2. 爬取网页内容

```bash
curl -X POST "http://localhost:8000/api/v1/crawl" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/article",
    "use_cache": true
  }'
```

### 3. 生成文章摘要

```bash
curl -X POST "http://localhost:8000/api/v1/summary" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "文章内容...",
    "title": "文章标题",
    "use_cache": true
  }'
```

### 4. 深度分析

```bash
curl -X POST "http://localhost:8000/api/v1/analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "文章内容...",
    "title": "文章标题",
    "use_cache": true
  }'
```

### 5. 关键词提取

```bash
curl -X POST "http://localhost:8000/api/v1/keywords" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "文章内容...",
    "title": "文章标题",
    "use_cache": true
  }'
```

### 6. 完整文章处理

```bash
curl -X POST "http://localhost:8000/api/v1/process" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/article",
    "use_cache": true
  }'
```

### 7. TLDR AI专用端点

```bash
curl http://localhost:8000/api/v1/tldr
```

## 测试

### 运行所有测试

```bash
# 使用uv运行pytest
uv run pytest

# 运行特定测试文件
uv run pytest tests/test_crawler.py

# 运行测试并显示覆盖率
uv run pytest --cov=src tests/
```

### 测试覆盖

- ✅ 网页爬取模块测试
- ✅ Azure OpenAI客户端测试  
- ✅ API端点测试
- ✅ 缓存管理测试
- ✅ 配置和日志测试

## 配置说明

### Azure OpenAI配置

```python
# 在.env文件中配置
AZURE_OPENAI_ENDPOINT=https://your-endpoint.cognitiveservices.azure.com/
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_MODEL_NAME=gpt-5
AZURE_OPENAI_DEPLOYMENT=gpt-5
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

### 爬虫配置

```python
CRAWLER_TARGET_URL=https://tldr.tech/ai/2025-10-03
CRAWLER_DELAY=1.0          # 请求间隔（秒）
CRAWLER_MAX_RETRIES=3      # 最大重试次数
CRAWLER_TIMEOUT=30         # 请求超时（秒）
```

### 缓存配置

```python
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=           # 可选
```

## 性能优化

1. **异步处理**: 所有IO操作都使用异步处理
2. **智能缓存**: Redis缓存爬取结果和AI处理结果
3. **请求限制**: 遵守robots.txt和请求间隔
4. **错误重试**: 自动重试机制处理临时错误
5. **连接池**: 复用HTTP连接提升性能

## 日志管理

日志文件位于`logs/`目录：
- `app.log`: 应用主日志
- 自动轮转和压缩
- 可配置日志级别

## 故障排除

### 常见问题

1. **Azure OpenAI连接失败**
   - 检查API密钥和端点配置
   - 确认模型部署名称正确

2. **Redis连接失败**
   - 检查Redis服务是否运行
   - 验证连接参数

3. **爬取失败**
   - 检查目标网站的robots.txt
   - 确认网络连接正常

### 调试模式

```bash
# 启用调试模式
export API_DEBUG=true
uv run python main.py
```

## 开发指南

### 添加新的AI处理功能

1. 在`src/ai/azure_openai_client.py`中添加新方法
2. 在`src/api/models.py`中定义请求/响应模型
3. 在`src/api/routes.py`中添加新端点
4. 编写相应的测试用例

### 扩展爬虫功能

1. 在`src/crawler/web_crawler.py`中添加新方法
2. 更新配置文件支持新参数
3. 添加相应的测试用例

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！