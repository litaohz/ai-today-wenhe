"""
Azure OpenAI客户端测试
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.ai.azure_openai_client import AzureOpenAIClient


class TestAzureOpenAIClient:
    """AzureOpenAIClient测试类"""
    
    @pytest.fixture
    def ai_client(self):
        """创建AI客户端实例"""
        return AzureOpenAIClient()
    
    def test_client_initialization(self, ai_client):
        """测试客户端初始化"""
        assert ai_client.client is not None
        assert hasattr(ai_client, 'model_name')
        assert hasattr(ai_client, 'deployment')
    
    @pytest.mark.asyncio
    @patch('openai.AsyncAzureOpenAI')
    async def test_generate_summary_success(self, mock_openai, ai_client):
        """测试成功生成摘要"""
        # 模拟OpenAI响应
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "这是一个测试摘要"
        
        mock_client = Mock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_openai.return_value = mock_client
        
        # 重新初始化客户端以使用模拟
        ai_client.client = mock_client
        
        result = await ai_client.generate_summary("测试内容", "测试标题")
        
        assert result == "这是一个测试摘要"
        mock_client.chat.completions.create.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('openai.AsyncAzureOpenAI')
    async def test_generate_summary_failure(self, mock_openai, ai_client):
        """测试摘要生成失败"""
        mock_client = Mock()
        mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API错误"))
        mock_openai.return_value = mock_client
        
        ai_client.client = mock_client
        
        result = await ai_client.generate_summary("测试内容", "测试标题")
        
        assert result is None
    
    @pytest.mark.asyncio
    @patch('openai.AsyncAzureOpenAI')
    async def test_generate_analysis_success(self, mock_openai, ai_client):
        """测试成功生成分析"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "这是一个深度分析"
        
        mock_client = Mock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_openai.return_value = mock_client
        
        ai_client.client = mock_client
        
        result = await ai_client.generate_analysis("测试内容", "测试标题")
        
        assert result == "这是一个深度分析"
    
    @pytest.mark.asyncio
    @patch('openai.AsyncAzureOpenAI')
    async def test_generate_keywords_success(self, mock_openai, ai_client):
        """测试成功生成关键词"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "人工智能,机器学习,深度学习"
        
        mock_client = Mock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_openai.return_value = mock_client
        
        ai_client.client = mock_client
        
        result = await ai_client.generate_keywords("测试内容", "测试标题")
        
        assert result == ["人工智能", "机器学习", "深度学习"]
    
    @pytest.mark.asyncio
    @patch('openai.AsyncAzureOpenAI')
    async def test_process_article_success(self, mock_openai, ai_client):
        """测试成功处理文章"""
        # 模拟所有AI响应
        mock_summary_response = Mock()
        mock_summary_response.choices = [Mock()]
        mock_summary_response.choices[0].message.content = "测试摘要"
        
        mock_analysis_response = Mock()
        mock_analysis_response.choices = [Mock()]
        mock_analysis_response.choices[0].message.content = "测试分析"
        
        mock_keywords_response = Mock()
        mock_keywords_response.choices = [Mock()]
        mock_keywords_response.choices[0].message.content = "关键词1,关键词2"
        
        mock_client = Mock()
        mock_client.chat.completions.create = AsyncMock(
            side_effect=[mock_summary_response, mock_analysis_response, mock_keywords_response]
        )
        mock_openai.return_value = mock_client
        
        ai_client.client = mock_client
        
        article_data = {
            'title': '测试文章',
            'content': '这是测试内容',
            'url': 'https://example.com',
            'word_count': 10,
            'crawled_at': 1234567890
        }
        
        result = await ai_client.process_article(article_data)
        
        assert result['original_data'] == article_data
        assert result['summary'] == "测试摘要"
        assert result['analysis'] == "测试分析"
        assert result['keywords'] == ["关键词1", "关键词2"]
        assert 'processing_time' in result
        assert 'processed_at' in result
    
    @pytest.mark.asyncio
    async def test_create_prompt(self, ai_client):
        """测试提示词创建"""
        content = "测试内容"
        title = "测试标题"
        prompt_type = "summary"
        
        prompt = ai_client._create_prompt(content, title, prompt_type)
        
        assert isinstance(prompt, list)
        assert len(prompt) == 2
        assert prompt[0]['role'] == 'system'
        assert prompt[1]['role'] == 'user'
        assert title in prompt[1]['content']
        assert content in prompt[1]['content']
    
    def test_parse_keywords(self, ai_client):
        """测试关键词解析"""
        # 测试逗号分隔
        keywords_str = "关键词1,关键词2,关键词3"
        result = ai_client._parse_keywords(keywords_str)
        assert result == ["关键词1", "关键词2", "关键词3"]
        
        # 测试换行分隔
        keywords_str = "关键词1\n关键词2\n关键词3"
        result = ai_client._parse_keywords(keywords_str)
        assert result == ["关键词1", "关键词2", "关键词3"]
        
        # 测试混合分隔符
        keywords_str = "关键词1, 关键词2\n关键词3"
        result = ai_client._parse_keywords(keywords_str)
        assert len(result) == 3
        
        # 测试空字符串
        result = ai_client._parse_keywords("")
        assert result == []