"""
Azure OpenAI 集成模块
"""
import asyncio
from typing import Dict, List, Optional, Any
from openai import AzureOpenAI
from config import settings, app_logger


class AzureOpenAIClient:
    """Azure OpenAI 客户端"""
    
    def __init__(self):
        self.client = AzureOpenAI(
            api_version=settings.azure_openai.api_version,
            azure_endpoint=settings.azure_openai.endpoint,
            api_key=settings.azure_openai.api_key,
        )
        app_logger.info("Azure OpenAI 客户端初始化完成")
        
    def _create_summary_prompt(self, content: str, title: str = "") -> List[Dict[str, str]]:
        """创建摘要生成的提示词"""
        system_prompt = """你是一个专业的AI技术资讯摘要助手。你将处理TLDR AI等技术newsletter的内容，这些内容通常包含多个分类的技术文章。

摘要要求：
1. **格式要求**：使用Markdown格式输出，包括标题、列表、加粗等
2. **长度控制**：300-400字之间
3. **结构组织**：按照内容分类组织摘要（如Headlines & Launches、Deep Dives & Analysis等）
4. **核心信息**：突出每个分类中的核心技术动态和重要信息
5. **关键术语**：保留关键的技术术语、公司名称、产品名称，使用**加粗**标记重要内容
6. **数据体现**：如果包含数据或统计信息，请在摘要中体现
7. **语言风格**：使用清晰易懂的中文，保持客观中性的语调
8. **重点领域**：重点关注AI、机器学习、技术创新等领域的最新动态
9. **引用标记**：在提及具体文章或重要信息时，使用[1]、[2]等数字标记进行引用
10. **标题翻译**：所有英文标题和分类名称必须翻译为中文，包括但不限于：
    - "Headlines & Launches" → "头条新闻与产品发布"
    - "Deep Dives & Analysis" → "深度分析"
    - "Engineering & Research" → "工程与研究"
    - "Miscellaneous" → "其他资讯"
    - "Quick Links" → "快速链接"
    - 所有文章标题都要翻译为中文

输出格式示例：
## 🚀 头条新闻与产品发布
- **OpenAI**发布了新的GPT模型[1]，性能提升显著
- **Google**推出了新的AI工具[2]，专注于代码生成

## 🔍 深度分析  
- 研究显示LLM在特定任务上的表现[3]
- 分析了AI应用的投资趋势[4]

请严格按照Markdown格式输出，确保引用标记的正确使用，并将所有英文标题翻译为中文。"""

        user_prompt = f"""请为以下技术newsletter生成结构化的Markdown格式摘要：

{content}

请生成一个按分类组织的中文Markdown摘要，并在适当位置添加引用标记："""

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
    def _create_analysis_prompt(self, content: str, title: str = "") -> List[Dict[str, str]]:
        """创建深度分析的提示词"""
        system_prompt = """你是一个专业的AI技术趋势分析师。你将分析TLDR AI等技术newsletter的内容，识别技术发展趋势和行业动态。

分析要求：
1. **技术趋势分析**: 识别AI、机器学习、技术创新等领域的最新趋势
2. **行业动态**: 分析公司动态、产品发布、融资等商业信息
3. **技术深度**: 对重要技术概念进行解释和分析
4. **影响评估**: 评估这些动态对行业和技术发展的潜在影响
5. **关联分析**: 分析不同技术动态之间的关联性
6. **未来展望**: 基于当前动态预测可能的发展方向
7. **标题翻译**: 在分析中提及英文标题时，必须翻译为中文，确保中文用户的阅读体验

请用中文进行分析，保持专业、客观、深入的分析视角。重点关注技术创新的价值和影响。在分析中提及文章标题时，请将英文标题翻译为中文。"""

        user_prompt = f"""请对以下技术newsletter进行深度分析：

{content}

请提供专业的技术趋势分析："""

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
    async def generate_summary(self, content: str, title: str = "") -> Optional[str]:
        """生成文章摘要"""
        try:
            app_logger.info(f"开始生成摘要，内容长度: {len(content)} 字符")
            
            messages = self._create_summary_prompt(content, title)
            
            # 使用线程池执行同步调用
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    messages=messages,
                    max_completion_tokens=settings.azure_openai.max_tokens,
                    model=settings.azure_openai.deployment
                )
            )
            
            summary = response.choices[0].message.content.strip()
            app_logger.info(f"摘要生成成功，长度: {len(summary)} 字符")
            
            return summary
            
        except Exception as e:
            app_logger.error(f"摘要生成失败: {e}")
            return None
            
    async def generate_analysis(self, content: str, title: str = "") -> Optional[str]:
        """生成深度分析"""
        try:
            app_logger.info(f"开始生成分析，内容长度: {len(content)} 字符")
            
            messages = self._create_analysis_prompt(content, title)
            
            # 使用线程池执行同步调用
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    messages=messages,
                    max_completion_tokens=settings.azure_openai.max_tokens,
                    model=settings.azure_openai.deployment
                )
            )
            
            analysis = response.choices[0].message.content.strip()
            app_logger.info(f"分析生成成功，长度: {len(analysis)} 字符")
            
            return analysis
            
        except Exception as e:
            app_logger.error(f"分析生成失败: {e}")
            return None
            
    async def generate_keywords(self, content: str, title: str = "") -> Optional[List[str]]:
        """提取关键词"""
        try:
            app_logger.info("开始提取关键词")
            
            system_prompt = """你是一个专业的AI技术关键词提取助手。请从技术newsletter中提取8-15个最重要的关键词。

要求：
1. 优先提取AI、机器学习、技术创新相关的术语
2. 包含重要的公司名称（如OpenAI、Anthropic、Google等）
3. 包含产品名称和技术概念（如GPT、Claude、LLM等）
4. 包含技术领域和应用场景
5. 避免过于通用的词汇（如"技术"、"发展"等）
6. 用逗号分隔关键词
7. 只输出关键词，不需要其他内容
8. 关键词应该能够代表当前AI技术发展的热点和趋势"""

            user_prompt = f"""请从以下技术newsletter中提取关键词：

{content}

请提取关键词："""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # 使用线程池执行同步调用
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    messages=messages,
                    max_completion_tokens=settings.azure_openai.max_tokens,
                    model=settings.azure_openai.deployment
                )
            )
            
            keywords_text = response.choices[0].message.content.strip()
            keywords = [kw.strip() for kw in keywords_text.split(',') if kw.strip()]
            
            app_logger.info(f"关键词提取成功: {keywords}")
            return keywords
            
        except Exception as e:
            app_logger.error(f"关键词提取失败: {e}")
            return None
            
    def _organize_content_for_llm(self, article_data: Dict[str, Any]) -> str:
        """组织content用于LLM分析，优先使用subtitle和sections"""
        try:
            # 获取基本信息
            title = article_data.get('title', '')
            subtitle = article_data.get('subtitle', '')
            sections = article_data.get('sections', [])
            
            # 构建结构化content
            organized_content = []
            
            # 添加标题和副标题
            if title:
                organized_content.append(f"标题: {title}")
            if subtitle:
                organized_content.append(f"副标题: {subtitle}")
                
            organized_content.append("")  # 空行分隔
            
            # 添加翻译指示
            organized_content.append("注意：以下内容包含英文标题，请在处理时将所有英文标题翻译为中文。")
            organized_content.append("")  # 空行分隔
            
            # 添加sections内容
            if sections:
                organized_content.append("主要内容分类:")
                for section in sections:
                    section_title = section.get('title', '')
                    articles = section.get('articles', [])
                    
                    if section_title and articles:  # 只处理有文章的section
                        organized_content.append(f"\n## {section_title}")
                        
                        for article in articles:
                            article_title = article.get('title', '')
                            article_content = article.get('content', '')
                            
                            if article_title:
                                organized_content.append(f"- {article_title}")
                            if article_content:
                                organized_content.append(f"  {article_content}")
            else:
                # 如果没有sections，使用原始content作为fallback
                original_content = article_data.get('content', '')
                if original_content:
                    organized_content.append("内容:")
                    organized_content.append(original_content)
                    
            return "\n".join(organized_content)
            
        except Exception as e:
            app_logger.error(f"内容组织失败: {e}")
            # 返回原始content作为fallback
            return article_data.get('content', '')

    def _extract_references_from_sections(self, sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """从sections中提取文章引用信息"""
        references = []
        ref_index = 1
        
        for section in sections:
            section_title = section.get('title', '')
            articles = section.get('articles', [])
            
            for article in articles:
                article_title = article.get('title', '')
                article_content = article.get('content', '')
                article_links = article.get('links', [])
                
                if article_title:  # 只有有标题的文章才作为引用
                    reference = {
                        'id': ref_index,
                        'title': article_title,
                        'content': article_content,
                        'section': section_title,
                        'links': article_links
                    }
                    references.append(reference)
                    ref_index += 1
                    
        return references

    async def process_article(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理文章数据，生成摘要、分析和关键词"""
        try:
            # 使用优化的content组织方法，直接覆盖原始content
            organized_content = self._organize_content_for_llm(article_data)
            title = article_data.get('title', '')
            
            if not organized_content:
                app_logger.warning("组织后的内容为空，跳过处理")
                return article_data
                
            # 直接用优化后的内容覆盖原始content
            content = organized_content
            
            # 提取引用信息
            sections = article_data.get('sections', [])
            references = self._extract_references_from_sections(sections)
            
            app_logger.info(f"开始处理文章: {title}")
            app_logger.info(f"优化后的内容长度: {len(content)} 字符")
            app_logger.info(f"提取到 {len(references)} 个引用")
            
            # 并发生成摘要、分析和关键词
            summary_task = self.generate_summary(content, title)
            analysis_task = self.generate_analysis(content, title)
            keywords_task = self.generate_keywords(content, title)
            
            summary, analysis, keywords = await asyncio.gather(
                summary_task, analysis_task, keywords_task,
                return_exceptions=True
            )
            
            # 处理结果
            processed_data = article_data.copy()
            processed_data['content'] = content
            processed_data['references'] = references  # 添加引用信息
            
            if not isinstance(summary, Exception) and summary:
                processed_data['summary'] = summary
            else:
                app_logger.error(f"摘要生成异常: {summary}")
                
            if not isinstance(analysis, Exception) and analysis:
                processed_data['analysis'] = analysis
            else:
                app_logger.error(f"分析生成异常: {analysis}")
                
            if not isinstance(keywords, Exception) and keywords:
                processed_data['keywords'] = keywords
            else:
                app_logger.error(f"关键词提取异常: {keywords}")
                
            processed_data['ai_processed'] = True
            processed_data['processing_timestamp'] = asyncio.get_event_loop().time()
            
            app_logger.info(f"文章处理完成: {title}")
            return processed_data
            
        except Exception as e:
            app_logger.error(f"文章处理失败: {e}")
            return article_data