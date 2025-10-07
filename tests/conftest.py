"""
pytest配置文件
"""
import pytest
import asyncio
import os
from unittest.mock import patch


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def mock_env_vars():
    """模拟环境变量"""
    with patch.dict(os.environ, {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_API_KEY': 'test-api-key',
        'AZURE_OPENAI_MODEL_NAME': 'gpt-5',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-5',
        'AZURE_OPENAI_API_VERSION': '2024-12-01-preview',
        'CRAWLER_TARGET_URL': 'https://tldr.tech/ai/2025-10-03',
        'CRAWLER_DELAY': '1.0',
        'CRAWLER_MAX_RETRIES': '3',
        'CRAWLER_TIMEOUT': '30',
        'REDIS_HOST': 'localhost',
        'REDIS_PORT': '6379',
        'REDIS_DB': '0',
        'API_HOST': '0.0.0.0',
        'API_PORT': '8000',
        'API_DEBUG': 'false',
        'LOG_LEVEL': 'INFO',
        'LOG_FILE': 'logs/app.log'
    }):
        yield


@pytest.fixture
def sample_article_data():
    """示例文章数据"""
    return {
        'title': '人工智能的未来发展趋势',
        'content': '''
        人工智能（AI）正在快速发展，并在各个领域产生深远影响。
        机器学习和深度学习技术的进步使得AI系统能够处理更复杂的任务。
        自然语言处理、计算机视觉和语音识别等技术已经在实际应用中取得显著成果。
        未来，AI将在医疗、教育、交通、金融等领域发挥更重要的作用。
        ''',
        'url': 'https://example.com/ai-future',
        'word_count': 50,
        'crawled_at': 1234567890
    }


@pytest.fixture
def sample_html_content():
    """示例HTML内容"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>测试文章标题</title>
        <meta charset="utf-8">
    </head>
    <body>
        <header>
            <nav>导航菜单</nav>
        </header>
        <main>
            <article>
                <h1>主要标题</h1>
                <p>这是第一段内容，包含重要信息。</p>
                <p>这是第二段内容，继续描述主题。</p>
                <div class="sidebar">
                    <p>侧边栏内容</p>
                </div>
            </article>
        </main>
        <footer>
            <p>页脚信息</p>
        </footer>
        <script>
            console.log('这是JavaScript代码');
        </script>
        <style>
            body { color: black; }
        </style>
    </body>
    </html>
    '''


@pytest.fixture
def sample_openai_response():
    """示例OpenAI响应"""
    class MockChoice:
        def __init__(self, content):
            self.message = type('Message', (), {'content': content})()
    
    class MockResponse:
        def __init__(self, content):
            self.choices = [MockChoice(content)]
    
    return MockResponse


@pytest.fixture
def sample_crawl_request():
    """示例爬取请求"""
    return {
        "url": "https://example.com/test-article",
        "use_cache": True
    }


@pytest.fixture
def sample_summary_request():
    """示例摘要请求"""
    return {
        "content": "这是一篇关于人工智能发展的文章内容...",
        "title": "人工智能的未来",
        "use_cache": True
    }


@pytest.fixture
def sample_analysis_request():
    """示例分析请求"""
    return {
        "content": "这是一篇关于人工智能发展的文章内容...",
        "title": "人工智能的未来",
        "use_cache": True
    }


@pytest.fixture
def sample_keywords_request():
    """示例关键词请求"""
    return {
        "content": "这是一篇关于人工智能发展的文章内容...",
        "title": "人工智能的未来",
        "use_cache": True
    }


@pytest.fixture
def sample_process_request():
    """示例处理请求"""
    return {
        "url": "https://example.com/test-article",
        "use_cache": True
    }