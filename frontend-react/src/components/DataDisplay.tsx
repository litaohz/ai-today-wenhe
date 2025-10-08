import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import rehypeRaw from 'rehype-raw';

const DisplayContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin-bottom: 2rem;
`;

const Panel = styled(motion.div)`
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid var(--neon-cyan);
  border-radius: 8px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  box-shadow: var(--box-glow);
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-pink), var(--neon-cyan));
    animation: borderScan 3s linear infinite;
  }
  
  @keyframes borderScan {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
  }
`;

const PanelTitle = styled.h3`
  font-family: 'Orbitron', monospace;
  color: var(--neon-cyan);
  text-shadow: var(--text-glow);
  margin-bottom: 1rem;
  font-size: 1.2rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  
  &::before {
    content: '▶ ';
    color: var(--neon-pink);
  }
`;

const PanelContent = styled.div`
  color: var(--text-primary);
  line-height: 1.8;
  font-size: 1rem;
`;

const MarkdownContainer = styled.div`
  color: var(--text-primary);
  line-height: 1.9;
  font-size: 1.05rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
  letter-spacing: 0.3px;
  word-spacing: 1px;

  /* Markdown 标题样式 */
  h1, h2, h3, h4, h5, h6 {
    color: var(--neon-cyan);
    font-family: 'Orbitron', monospace;
    text-shadow: var(--text-glow);
    margin: 1.5rem 0 1rem 0;
    font-weight: 600;
  }

  h1 { font-size: 1.8rem; border-bottom: 2px solid var(--neon-cyan); padding-bottom: 0.5rem; }
  h2 { font-size: 1.5rem; border-bottom: 1px solid rgba(0, 255, 255, 0.5); padding-bottom: 0.3rem; }
  h3 { font-size: 1.3rem; }
  h4 { font-size: 1.2rem; }
  h5 { font-size: 1.1rem; }
  h6 { font-size: 1rem; }

  /* 段落样式 */
  p {
    margin-bottom: 1.4rem;
    text-align: justify;
    text-indent: 0;
    padding: 0.3rem 0;
    
    &:first-child {
      margin-top: 0.5rem;
    }
    
    &:last-child {
      margin-bottom: 0.5rem;
    }
  }

  /* 列表样式 */
  ul, ol {
    margin: 1rem 0;
    padding-left: 2rem;
  }

  ul li {
    margin-bottom: 0.8rem;
    padding: 0.4rem 0 0.4rem 1rem;
    position: relative;
    background: rgba(255, 0, 255, 0.02);
    border-radius: 6px;
    border-left: 2px solid rgba(255, 0, 255, 0.3);
    list-style: none;

    &::before {
      content: '▶';
      position: absolute;
      left: -1.5rem;
      top: 0.4rem;
      color: var(--neon-pink);
      font-size: 0.9rem;
      transition: transform 0.3s ease;
    }

    &:hover {
      background: rgba(255, 0, 255, 0.05);
      border-left-color: var(--neon-pink);
      
      &::before {
        transform: translateX(2px);
      }
    }
  }

  ol li {
    margin-bottom: 1rem;
    padding: 0.5rem 0 0.5rem 1rem;
    position: relative;
    background: rgba(0, 255, 255, 0.02);
    border-radius: 6px;
    border-left: 2px solid rgba(0, 255, 255, 0.3);

    &:hover {
      background: rgba(0, 255, 255, 0.05);
      border-left-color: var(--neon-cyan);
    }
  }

  /* 引用样式 */
  blockquote {
    background: linear-gradient(135deg, rgba(0, 255, 255, 0.08), rgba(255, 0, 255, 0.08));
    padding: 1rem 1.5rem;
    border-radius: 8px;
    border-left: 4px solid var(--neon-cyan);
    margin: 1.5rem 0;
    position: relative;
    box-shadow: 0 2px 8px rgba(0, 255, 255, 0.1);
    font-style: italic;

    &::before {
      content: '"';
      position: absolute;
      left: 0.5rem;
      top: -0.5rem;
      font-size: 2rem;
      color: var(--neon-cyan);
      font-family: 'Orbitron', monospace;
    }

    p {
      margin: 0;
    }

    &:hover {
      background: linear-gradient(135deg, rgba(0, 255, 255, 0.12), rgba(255, 0, 255, 0.12));
      box-shadow: 0 4px 16px rgba(0, 255, 255, 0.2);
      transform: translateY(-1px);
    }
  }

  /* 代码样式 */
  code {
    background: rgba(0, 255, 255, 0.1);
    color: var(--neon-cyan);
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-family: 'Orbitron', monospace;
    font-size: 0.9em;
    border: 1px solid rgba(0, 255, 255, 0.3);
  }

  pre {
    background: rgba(0, 0, 0, 0.8);
    border: 1px solid var(--neon-cyan);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    overflow-x: auto;
    
    code {
      background: none;
      border: none;
      padding: 0;
      color: var(--text-primary);
    }
  }

  /* 强调样式 */
  strong, b {
    color: var(--neon-pink);
    font-weight: 600;
    text-shadow: 0 0 4px rgba(255, 0, 255, 0.3);
  }

  em, i {
    color: var(--neon-purple);
    font-style: italic;
  }

  /* 链接样式 */
  a {
    color: var(--neon-cyan);
    text-decoration: none;
    border-bottom: 1px solid rgba(0, 255, 255, 0.3);
    transition: all 0.3s ease;

    &:hover {
      color: var(--neon-pink);
      border-bottom-color: var(--neon-pink);
      text-shadow: 0 0 8px rgba(255, 0, 255, 0.4);
    }
  }

  /* 分隔线样式 */
  hr {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), var(--neon-pink), transparent);
    margin: 2rem 0;
    border: none;
    border-radius: 1px;
    position: relative;

    &::before {
      content: '';
      position: absolute;
      top: -1px;
      left: 50%;
      transform: translateX(-50%);
      width: 6px;
      height: 6px;
      background: var(--neon-cyan);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--neon-cyan);
    }
  }

  /* 表格样式 */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 8px;
    overflow: hidden;
  }

  th, td {
    padding: 0.8rem;
    text-align: left;
    border-bottom: 1px solid rgba(0, 255, 255, 0.3);
  }

  th {
    background: rgba(0, 255, 255, 0.1);
    color: var(--neon-cyan);
    font-family: 'Orbitron', monospace;
    font-weight: 600;
  }

  tr:hover {
    background: rgba(0, 255, 255, 0.05);
  }

  /* 引用标记样式 */
  .reference {
    display: inline-block;
    background: var(--neon-purple);
    color: white;
    padding: 0.1rem 0.3rem;
    border-radius: 3px;
    font-size: 0.8rem;
    font-weight: bold;
    margin: 0 0.2rem;
    text-decoration: none;
    transition: all 0.3s ease;
    vertical-align: super;
    line-height: 1;

    &:hover {
      background: var(--neon-pink);
      transform: scale(1.1);
      box-shadow: 0 0 8px rgba(255, 0, 255, 0.4);
    }
  }
`;

const FormattedText = styled.div`
  color: var(--text-primary);
  line-height: 1.9;
  font-size: 1.05rem;
  counter-reset: item-counter;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
  letter-spacing: 0.3px;
  word-spacing: 1px;
  
  p {
    margin-bottom: 1.4rem;
    text-align: justify;
    text-indent: 0;
    padding: 0.3rem 0;
    
    &:first-child {
      margin-top: 0.5rem;
    }
    
    &:last-child {
      margin-bottom: 0.5rem;
    }
  }
  
  /* 处理数字列表 */
  .numbered-item {
    margin-bottom: 1.2rem;
    padding: 0.5rem 0 0.5rem 2rem;
    position: relative;
    background: rgba(0, 255, 255, 0.02);
    border-radius: 6px;
    border-left: 2px solid rgba(0, 255, 255, 0.3);
    
    &::before {
      content: counter(item-counter) '. ';
      counter-increment: item-counter;
      position: absolute;
      left: 0.5rem;
      top: 0.5rem;
      color: var(--neon-cyan);
      font-weight: bold;
      font-size: 1.1rem;
      font-family: 'Orbitron', monospace;
    }
    
    &:hover {
      background: rgba(0, 255, 255, 0.05);
      border-left-color: var(--neon-cyan);
    }
  }
  
  /* 处理要点列表 */
  .bullet-item {
    margin-bottom: 1rem;
    padding: 0.4rem 0 0.4rem 1.8rem;
    position: relative;
    background: rgba(255, 0, 255, 0.02);
    border-radius: 6px;
    border-left: 2px solid rgba(255, 0, 255, 0.3);
    
    &::before {
      content: '▶';
      position: absolute;
      left: 0.5rem;
      top: 0.4rem;
      color: var(--neon-pink);
      font-size: 0.9rem;
      transition: transform 0.3s ease;
    }
    
    &:hover {
      background: rgba(255, 0, 255, 0.05);
      border-left-color: var(--neon-pink);
      
      &::before {
        transform: translateX(2px);
      }
    }
  }
  
  /* 高亮关键信息 */
  .highlight {
    background: linear-gradient(135deg, rgba(0, 255, 255, 0.08), rgba(255, 0, 255, 0.08));
    padding: 0.8rem 1rem;
    border-radius: 8px;
    border-left: 4px solid var(--neon-cyan);
    margin: 1.2rem 0;
    display: block;
    position: relative;
    box-shadow: 0 2px 8px rgba(0, 255, 255, 0.1);
    
    &::before {
      content: '💡';
      position: absolute;
      left: -2px;
      top: -8px;
      background: var(--bg-primary);
      padding: 0.2rem;
      border-radius: 50%;
      font-size: 0.8rem;
    }
    
    &:hover {
      background: linear-gradient(135deg, rgba(0, 255, 255, 0.12), rgba(255, 0, 255, 0.12));
      box-shadow: 0 4px 16px rgba(0, 255, 255, 0.2);
      transform: translateY(-1px);
    }
  }
  
  /* 分隔线 */
  .separator {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), var(--neon-pink), transparent);
    margin: 2rem 0;
    border-radius: 1px;
    position: relative;
    
    &::before {
      content: '';
      position: absolute;
      top: -1px;
      left: 50%;
      transform: translateX(-50%);
      width: 6px;
      height: 6px;
      background: var(--neon-cyan);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--neon-cyan);
    }
  }
  
  /* 公司名称高亮 */
  .company-name {
    color: var(--neon-purple);
    font-weight: 600;
    background: rgba(128, 0, 255, 0.1);
    padding: 0.1rem 0.3rem;
    border-radius: 3px;
    border-bottom: 1px solid var(--neon-purple);
    transition: all 0.3s ease;
    
    &:hover {
      background: rgba(128, 0, 255, 0.2);
      box-shadow: 0 0 8px rgba(128, 0, 255, 0.4);
    }
  }
  
  /* 数字和统计数据高亮 */
  .number {
    color: var(--neon-green);
    font-weight: 700;
    font-family: 'Orbitron', monospace;
    background: rgba(0, 255, 0, 0.1);
    padding: 0.1rem 0.3rem;
    border-radius: 3px;
    border: 1px solid rgba(0, 255, 0, 0.3);
    
    &:hover {
      background: rgba(0, 255, 0, 0.2);
      box-shadow: 0 0 6px rgba(0, 255, 0, 0.4);
    }
  }
  
  /* 重要关键词高亮 */
  .keyword {
    color: var(--neon-pink);
    font-weight: 600;
    background: rgba(255, 0, 255, 0.1);
    padding: 0.1rem 0.3rem;
    border-radius: 3px;
    border-bottom: 1px solid var(--neon-pink);
    text-shadow: 0 0 4px rgba(255, 0, 255, 0.3);
    
    &:hover {
      background: rgba(255, 0, 255, 0.2);
      box-shadow: 0 0 8px rgba(255, 0, 255, 0.4);
    }
  }
  
  /* 技术术语高亮 */
  .tech-term {
    color: var(--neon-cyan);
    font-weight: 600;
    font-family: 'Orbitron', monospace;
    background: rgba(0, 255, 255, 0.1);
    padding: 0.1rem 0.3rem;
    border-radius: 3px;
    border: 1px solid rgba(0, 255, 255, 0.3);
    text-transform: uppercase;
    font-size: 0.9em;
    letter-spacing: 0.5px;
    
    &:hover {
      background: rgba(0, 255, 255, 0.2);
      box-shadow: 0 0 8px rgba(0, 255, 255, 0.4);
      transform: translateY(-1px);
    }
  }
`;

const KeywordContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
`;

const Keyword = styled(motion.span)`
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid var(--neon-cyan);
  color: var(--neon-cyan);
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-family: 'Orbitron', monospace;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(0, 255, 255, 0.2);
    box-shadow: 0 0 10px var(--neon-cyan);
    transform: translateY(-2px);
  }
`;

const ArticleList = styled.div`
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid var(--neon-green);
  border-radius: 8px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
  margin-top: 2rem;
`;

const ArticleItem = styled(motion.div)`
  border-bottom: 1px solid rgba(0, 255, 0, 0.3);
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 8px;
  transition: all 0.3s ease;
  position: relative;
  
  &:last-child {
    border-bottom: 1px solid rgba(0, 255, 0, 0.3);
  }
  
  &.clickable:hover {
    background: rgba(0, 255, 0, 0.1);
    border: 1px solid var(--neon-green);
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
    transform: translateY(-2px);
  }
  
  &.non-clickable:hover {
    background: rgba(0, 255, 0, 0.05);
    border: 1px solid rgba(0, 255, 0, 0.5);
  }
  
  &.clickable::after {
    content: '🔗';
    position: absolute;
    top: 1rem;
    right: 1rem;
    color: var(--neon-green);
    opacity: 0;
    transition: opacity 0.3s ease;
    font-size: 1rem;
  }
  
  &.clickable:hover::after {
    opacity: 1;
  }
  
  &.non-clickable::after {
    content: '📄';
    position: absolute;
    top: 1rem;
    right: 1rem;
    color: rgba(0, 255, 0, 0.5);
    opacity: 0.3;
    font-size: 1rem;
  }
`;

const ArticleTitle = styled.h4`
  color: var(--neon-green);
  font-family: 'Orbitron', monospace;
  margin-bottom: 0.5rem;
  font-size: 1rem;
  text-shadow: var(--text-glow);
`;

const ArticleDescription = styled.p`
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.4;
`;

const LinkContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
`;

const LinkCard = styled(motion.a)`
  display: block;
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid var(--neon-purple);
  border-radius: 8px;
  padding: 1rem;
  text-decoration: none;
  color: var(--text-primary);
  backdrop-filter: blur(10px);
  box-shadow: 0 0 20px rgba(128, 0, 255, 0.3);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 30px rgba(128, 0, 255, 0.5);
    border-color: var(--neon-pink);
  }
`;

const LinkTitle = styled.h4`
  color: var(--neon-purple);
  font-family: 'Orbitron', monospace;
  margin-bottom: 0.5rem;
  font-size: 1rem;
  text-shadow: var(--text-glow);
`;

const LinkDescription = styled.p`
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.4;
`;

// 引用弹窗样式
const ReferenceModal = styled(motion.div)`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(10px);
`;

const ReferenceContent = styled(motion.div)`
  background: rgba(0, 0, 0, 0.9);
  border: 2px solid var(--neon-cyan);
  border-radius: 12px;
  padding: 2rem;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
`;

const ReferenceHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
`;

const ReferenceTitle = styled.h3`
  color: var(--neon-cyan);
  font-family: 'Orbitron', monospace;
  font-size: 1.3rem;
  margin: 0;
  text-shadow: var(--text-glow);
  flex: 1;
  margin-right: 1rem;
`;

const CloseButton = styled.button`
  background: none;
  border: 2px solid var(--neon-pink);
  color: var(--neon-pink);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  
  &:hover {
    background: var(--neon-pink);
    color: black;
    box-shadow: 0 0 15px var(--neon-pink);
  }
`;

const ReferenceSection = styled.div`
  color: var(--neon-purple);
  font-size: 0.9rem;
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  background: rgba(128, 0, 255, 0.1);
  border-radius: 6px;
  border-left: 3px solid var(--neon-purple);
`;

const ReferenceText = styled.div`
  color: var(--text-primary);
  line-height: 1.8;
  margin-bottom: 1.5rem;
  font-size: 1rem;
`;

const ReferenceLinks = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
`;

const ReferenceLink = styled.a`
  color: var(--neon-green);
  text-decoration: none;
  padding: 0.8rem 1rem;
  background: rgba(0, 255, 0, 0.1);
  border: 1px solid rgba(0, 255, 0, 0.3);
  border-radius: 6px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  &:hover {
    background: rgba(0, 255, 0, 0.2);
    border-color: var(--neon-green);
    box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
    transform: translateX(5px);
  }
  
  &::before {
    content: '🔗';
    font-size: 1rem;
  }
`;

interface Reference {
  index: number;
  title: string;
  content: string;
  section: string;
  url: string;
}

interface DataDisplayProps {
  summary?: string;
  analysis?: string;
  keywords?: string[];
  references?: Reference[];
  articles?: Array<{
    title: string;
    content: string;
    links?: Array<{
      url: string;
      text: string;
    }>;
    word_count?: number;
  }>;
  sections?: Array<{
    title: string;
    articles: Array<{
      title: string;
      content: string;
      links?: Array<{
        url: string;
        text: string;
      }>;
      word_count?: number;
    }>;
    article_count: number;
  }>;
  links?: Array<{
    title: string;
    description: string;
    url: string;
  }>;
}

const DataDisplay: React.FC<DataDisplayProps> = ({
  summary = "正在加载摘要数据...",
  analysis = "正在加载分析数据...",
  keywords = [],
  references = [],
  articles = [],
  sections = [],
  links = []
}) => {
  const [selectedReference, setSelectedReference] = useState<Reference | null>(null);
  
  // 添加ESC键监听来关闭弹窗
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && selectedReference) {
        setSelectedReference(null);
      }
    };

    if (selectedReference) {
      document.addEventListener('keydown', handleKeyDown);
    }

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [selectedReference]);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.6
      }
    }
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <DisplayContainer>
        <Panel variants={itemVariants}>
          <PanelTitle>AI 摘要</PanelTitle>
          {renderMarkdown(summary, references, setSelectedReference)}
        </Panel>

        {/* 暂时注释掉深度分析模块 */}
        {/* <Panel variants={itemVariants}>
          <PanelTitle>深度分析</PanelTitle>
          {formatText(analysis)}
        </Panel> */}
      </DisplayContainer>



      {/* {references && references.length > 0 && (
        <Panel variants={itemVariants}>
          <PanelTitle>参考文献 ({references.length})</PanelTitle>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {references.map((reference, index) => (
              <div
                key={reference.id}
                style={{
                  background: 'rgba(0, 255, 255, 0.1)',
                  border: '1px solid var(--neon-cyan)',
                  borderRadius: '4px',
                  padding: '1rem',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease'
                }}
                onClick={() => setSelectedReference(reference)}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'rgba(0, 255, 255, 0.2)';
                  e.currentTarget.style.transform = 'translateX(5px)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'rgba(0, 255, 255, 0.1)';
                  e.currentTarget.style.transform = 'translateX(0)';
                }}
              >
                <div style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '1rem'
                }}>
                  <span style={{
                    color: 'var(--neon-pink)',
                    fontWeight: 'bold',
                    fontSize: '0.9rem',
                    minWidth: '30px',
                    textAlign: 'center',
                    background: 'rgba(255, 20, 147, 0.2)',
                    borderRadius: '50%',
                    padding: '4px 8px'
                  }}>
                    [{reference.id}]
                  </span>
                  <div style={{ flex: 1 }}>
                    <h4 style={{
                      color: 'var(--neon-cyan)',
                      margin: '0 0 0.5rem 0',
                      fontSize: '1rem',
                      fontWeight: 'bold'
                    }}>
                      {reference.title}
                    </h4>
                    {reference.section && (
                      <div style={{
                        color: 'var(--neon-green)',
                        fontSize: '0.8rem',
                        marginBottom: '0.5rem',
                        opacity: 0.8
                      }}>
                        分类: {reference.section}
                      </div>
                    )}
                    <p style={{
                      color: '#ffffff',
                      margin: '0',
                      fontSize: '0.9rem',
                      lineHeight: '1.4',
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      overflow: 'hidden'
                    }}>
                      {reference.content}
                    </p>
                    {reference.links && reference.links.length > 0 && (
                      <div style={{ marginTop: '0.5rem' }}>
                        {reference.links.slice(0, 2).map((link, linkIndex) => (
                          <a
                            key={linkIndex}
                            href={link.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            onClick={(e) => e.stopPropagation()}
                            style={{
                              color: 'var(--neon-green)',
                              textDecoration: 'none',
                              fontSize: '0.8rem',
                              marginRight: '1rem',
                              display: 'inline-block'
                            }}
                          >
                            🔗 {link.text}
                          </a>
                        ))}
                        {reference.links.length > 2 && (
                          <span style={{
                            color: 'var(--neon-cyan)',
                            fontSize: '0.8rem',
                            opacity: 0.7
                          }}>
                            +{reference.links.length - 2} 更多链接
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Panel>
      )} */}

      {/* {sections && sections.length > 0 && (
        <Panel
          variants={itemVariants}
          initial="hidden"
          animate="visible"
        >
          <PanelTitle>相关文章</PanelTitle>
          {sections.filter(section => section.title || (section.articles && section.articles.length > 0)).map((section, sectionIndex) => (
            <div key={sectionIndex} style={{ marginBottom: '2rem' }}>
              <h3 style={{ 
                color: 'var(--neon-cyan)', 
                fontSize: '1.2rem', 
                marginBottom: '1rem',
                borderBottom: '1px solid var(--neon-cyan)',
                paddingBottom: '0.5rem'
              }}>
                {section.title || '未分类内容'} ({section.article_count} 篇文章)
              </h3>
              {section.articles && section.articles.length > 0 && (
                <ArticleList
                  variants={containerVariants}
                  initial="hidden"
                  animate="visible"
                >
                  {section.articles.map((article, articleIndex) => {
                    // 获取第一个可用的链接
                    const firstLink = article.links && article.links.length > 0 ? article.links[0].url : null;
                    
                    const handleCardClick = () => {
                      if (firstLink) {
                        window.open(firstLink, '_blank', 'noopener,noreferrer');
                      }
                    };

                    return (
                      <ArticleItem
                         key={articleIndex}
                         variants={itemVariants}
                         whileHover={firstLink ? { x: 10, scale: 1.02 } : { x: 5 }}
                         onClick={handleCardClick}
                         style={{ 
                           cursor: firstLink ? 'pointer' : 'default',
                           position: 'relative',
                           opacity: firstLink ? 1 : 0.8
                         }}
                         className={firstLink ? 'clickable' : 'non-clickable'}
                       >
                      <ArticleTitle>{article.title}</ArticleTitle>
                      <ArticleDescription>{article.content}</ArticleDescription>
                      {article.word_count && (
                        <div style={{ 
                          color: 'var(--neon-cyan)', 
                          fontSize: '0.8rem', 
                          marginTop: '0.5rem' 
                        }}>
                          字数: {article.word_count}
                        </div>
                      )}
                      {article.links && article.links.length > 0 && (
                        <div style={{ marginTop: '0.5rem' }}>
                          {article.links.map((link, linkIndex) => (
                            <a
                              key={linkIndex}
                              href={link.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              style={{
                                color: 'var(--neon-green)',
                                textDecoration: 'none',
                                fontSize: '0.8rem',
                                marginRight: '1rem',
                                display: 'inline-block'
                              }}
                            >
                              🔗 {link.text}
                            </a>
                          ))}
                        </div>
                      )}
                    </ArticleItem>
                    );
                  })}
                </ArticleList>
              )}
            </div>
          ))}
        </Panel>
      )} */}

      {links.length > 0 && (
        <LinkContainer>
          {links.map((link, index) => (
            <LinkCard
              key={index}
              href={link.url}
              target="_blank"
              rel="noopener noreferrer"
              variants={itemVariants}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <LinkTitle>{link.title}</LinkTitle>
              <LinkDescription>{link.description}</LinkDescription>
            </LinkCard>
          ))}
        </LinkContainer>
      )}

      {/* 引用弹窗 */}
      {selectedReference && (
        <ReferenceModal
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => setSelectedReference(null)}
        >
          <ReferenceContent
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.8, opacity: 0 }}
            onClick={(e) => e.stopPropagation()}
          >
            <ReferenceHeader>
              <ReferenceTitle>{selectedReference.title}</ReferenceTitle>
              <CloseButton onClick={() => setSelectedReference(null)}>
                ×
              </CloseButton>
            </ReferenceHeader>
            
            <ReferenceSection>
              来源分类: {selectedReference.section}
            </ReferenceSection>
            
            <ReferenceText>
              {selectedReference.content}
            </ReferenceText>
            
            {selectedReference.url && (
              <ReferenceLinks>
                <ReferenceLink
                  href={selectedReference.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  查看原文
                </ReferenceLink>
              </ReferenceLinks>
            )}
          </ReferenceContent>
        </ReferenceModal>
      )}
    </motion.div>
  );
};

// 文本格式化函数
// 新的Markdown渲染函数
const renderMarkdown = (
  text: string, 
  references: Reference[] = [], 
  setSelectedReference?: (ref: Reference | null) => void
): JSX.Element => {
  if (!text) return <span>暂无内容</span>;
  
  // 处理引用标记 [1], [2] 等
  const processReferences = (content: string): string => {
    const result = content.replace(/\[(\d+)\]/g, (match, refId) => {
      const refNumber = parseInt(refId);
      const reference = references?.find(ref => ref.index === refNumber);
      
      if (reference) {
        return `<span class="reference" data-ref-id="${refId}">${refId}</span>`;
      }
      return match;
    });
    
    return result;
  };

  // 自定义组件来处理引用
  const components = {
    span: ({ className, children, ...props }: any) => {
      if (className === 'reference') {
        const refId = parseInt(props['data-ref-id']);
        const reference = references.find(ref => ref.index === refId);
        
        return (
          <span 
            className="reference" 
            onClick={() => {
              if (reference && setSelectedReference) {
                setSelectedReference(reference);
              } else {
                console.log(`引用 [${children}] 未找到对应的文章信息`);
              }
            }}
            style={{ cursor: reference ? 'pointer' : 'default' }}
            title={reference ? `点击查看: ${reference.title}` : '引用信息不可用'}
            {...props}
          >
            {children}
          </span>
        );
      }
      return <span className={className} {...props}>{children}</span>;
    }
  };

  const processedText = processReferences(text);

  return (
    <MarkdownContainer>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw, rehypeHighlight]}
        components={components}
      >
        {processedText}
      </ReactMarkdown>
    </MarkdownContainer>
  );
};

const formatText = (text: string): JSX.Element => {
  if (!text) return <span>暂无内容</span>;
  
  // 智能段落分割
  const smartSplit = (text: string): string[] => {
    // 先按标点符号分割
    const sentences = text.split(/([。！？；])/);
    const paragraphs: string[] = [];
    let currentParagraph = '';
    
    for (let i = 0; i < sentences.length; i += 2) {
      const sentence = sentences[i];
      const punctuation = sentences[i + 1] || '';
      
      if (sentence && sentence.trim()) {
        currentParagraph += sentence + punctuation;
        
        // 段落分割条件
        const shouldSplit = 
          currentParagraph.length > 120 || // 长度超过120字符
          /[。！？]$/.test(currentParagraph) && (
            // 遇到段落转换关键词
            /总结|分析|此外|另外|同时|然而|因此|首先|其次|最后|综上|总的来说|具体来说|值得注意的是|需要指出的是/.test(currentParagraph) ||
            // 或者包含数字序号
            /\d+[、.]/.test(currentParagraph)
          );
        
        if (shouldSplit) {
          paragraphs.push(currentParagraph.trim());
          currentParagraph = '';
        }
      }
    }
    
    if (currentParagraph.trim()) {
      paragraphs.push(currentParagraph.trim());
    }
    
    return paragraphs;
  };
  
  // 高亮关键词和实体
  const highlightKeywords = (text: string): JSX.Element => {
    // 定义需要高亮的模式
    const patterns = [
      // 公司名称 (包含常见后缀)
      { regex: /([A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*(?:\s+(?:Inc|Corp|Ltd|LLC|Co|Company|Technologies|Tech|Systems|Solutions|Group|Holdings|Ventures|Capital|Partners|Labs|Studio|AI|Labs))?)/g, className: 'company-name' },
      // 中文公司名称
      { regex: /([\u4e00-\u9fa5]+(?:公司|科技|技术|集团|控股|投资|资本|实验室|工作室|平台|网络|系统|解决方案))/g, className: 'company-name' },
      // 数字和百分比
      { regex: /(\d+(?:\.\d+)?(?:%|亿|万|千|百|美元|元|USD|CNY|billion|million|thousand))/g, className: 'number' },
      // 重要关键词
      { regex: /(重要|关键|核心|主要|显著|突出|创新|突破|领先|首次|最新|发布|推出|宣布|获得|达成|实现|增长|下降|上涨|下跌)/g, className: 'keyword' },
      // 技术术语
      { regex: /(AI|人工智能|机器学习|深度学习|神经网络|算法|数据|云计算|区块链|物联网|5G|6G|VR|AR|元宇宙|ChatGPT|GPT|LLM|API|SDK|开源|闭源)/g, className: 'tech-term' }
    ];
    
    let result = text;
    let elements: JSX.Element[] = [];
    let lastIndex = 0;
    
    // 收集所有匹配项
    const matches: Array<{start: number, end: number, text: string, className: string}> = [];
    
    patterns.forEach(pattern => {
      let match;
      while ((match = pattern.regex.exec(text)) !== null) {
        matches.push({
          start: match.index,
          end: match.index + match[0].length,
          text: match[0],
          className: pattern.className
        });
      }
    });
    
    // 按位置排序并去重
    matches.sort((a, b) => a.start - b.start);
    const uniqueMatches = matches.filter((match, index) => {
      return index === 0 || match.start >= matches[index - 1].end;
    });
    
    // 构建JSX元素
    uniqueMatches.forEach((match, index) => {
      // 添加匹配前的普通文本
      if (match.start > lastIndex) {
        elements.push(<span key={`text-${index}`}>{text.slice(lastIndex, match.start)}</span>);
      }
      
      // 添加高亮的匹配文本
      elements.push(
        <span key={`highlight-${index}`} className={match.className}>
          {match.text}
        </span>
      );
      
      lastIndex = match.end;
    });
    
    // 添加最后的普通文本
    if (lastIndex < text.length) {
      elements.push(<span key="text-final">{text.slice(lastIndex)}</span>);
    }
    
    return elements.length > 0 ? <>{elements}</> : <span>{text}</span>;
  };
  
  const paragraphs = smartSplit(text);
  
  return (
    <FormattedText>
      {paragraphs.map((paragraph, index) => {
        // 检查是否是数字开头的列表项
        if (/^\d+[、.]/.test(paragraph)) {
          return (
            <div key={index} className="numbered-item">
              {highlightKeywords(paragraph.replace(/^\d+[、.]/, '').trim())}
            </div>
          );
        }
        
        // 检查是否是要点列表
        if (/^[·•-]/.test(paragraph)) {
          return (
            <div key={index} className="bullet-item">
              {highlightKeywords(paragraph.replace(/^[·•-]/, '').trim())}
            </div>
          );
        }
        
        // 检查是否包含重要信息关键词
        const isHighlight = /重要|关键|核心|主要|显著|突出|总结|结论/.test(paragraph);
        
        return (
          <div key={index}>
            {index > 0 && index % 4 === 0 && <div className="separator" />}
            <p className={isHighlight ? 'highlight' : ''}>
              {highlightKeywords(paragraph)}
            </p>
          </div>
        );
      })}
    </FormattedText>
  );
};

export default DataDisplay;