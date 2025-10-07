import { useEffect, useState } from 'react';
import ParticleBackground from './components/ParticleBackground';
import CyberpunkLayout from './components/CyberpunkLayout';
import DataDisplay from './components/DataDisplay';
import DatePicker from './components/DatePicker';
import DebugPanel from './components/DebugPanel';
import { useAppStore } from './store/appStore';

// 示例数据作为后备
const exampleData = {
  summary: "今日AI领域重要进展：OpenAI发布GPT-4 Turbo新版本，性能提升显著；Google DeepMind在蛋白质折叠预测方面取得突破；Meta推出新的多模态AI模型；微软Azure AI服务扩展到更多地区。这些发展标志着AI技术在各个领域的快速进步。",
  analysis: "当前AI发展呈现几个重要趋势：1) 大语言模型持续优化，成本效益比不断提升；2) 多模态AI成为主流，文本、图像、音频融合处理能力增强；3) AI基础设施建设加速，云服务商竞争激烈；4) 行业应用深化，从通用工具向专业解决方案演进。预计未来6个月内，AI Agent和实时推理能力将成为竞争焦点。",
  keywords: ["GPT-4 Turbo", "多模态AI", "蛋白质折叠", "Azure AI", "实时推理", "AI Agent", "深度学习", "机器学习"],
  articles: [
    {
      title: "OpenAI GPT-4 Turbo 性能评测",
      content: "详细分析新版本在推理速度、准确性和成本控制方面的改进。新版本在多个基准测试中表现出色，推理速度提升40%，同时保持了高准确性。成本控制方面，相比前一版本降低了30%的使用成本。",
      word_count: 120
    },
    {
      title: "Google DeepMind 蛋白质研究突破",
      content: "AlphaFold 3.0 在药物发现领域的最新应用成果。新版本能够预测更复杂的蛋白质结构，准确率达到95%以上，为新药研发提供了强有力的工具支持。",
      word_count: 85
    },
    {
      title: "Meta 多模态AI模型发布",
      content: "新模型在图像理解和文本生成方面的创新特性。该模型能够同时处理文本、图像和音频输入，在多模态任务中表现出色，为AI应用开辟了新的可能性。",
      word_count: 95
    }
  ],
  sections: [
    {
      title: "头条新闻",
      article_count: 2,
      articles: [
        {
          title: "OpenAI GPT-4 Turbo 性能评测",
          content: "详细分析新版本在推理速度、准确性和成本控制方面的改进。新版本在多个基准测试中表现出色，推理速度提升40%，同时保持了高准确性。",
          word_count: 120,
          links: [
            { url: "https://openai.com/gpt-4-turbo", text: "官方发布页面" },
            { url: "https://platform.openai.com/docs", text: "技术文档" }
          ]
        },
        {
          title: "Google DeepMind 蛋白质研究突破",
          content: "AlphaFold 3.0 在药物发现领域的最新应用成果。新版本能够预测更复杂的蛋白质结构，准确率达到95%以上。",
          word_count: 85,
          links: [
            { url: "https://deepmind.com/alphafold", text: "AlphaFold 官网" }
          ]
        }
      ]
    },
    {
      title: "技术深度",
      article_count: 1,
      articles: [
        {
          title: "Meta 多模态AI模型发布",
          content: "新模型在图像理解和文本生成方面的创新特性。该模型能够同时处理文本、图像和音频输入，在多模态任务中表现出色。",
          word_count: 95,
          links: [
            { url: "https://ai.meta.com", text: "Meta AI 研究" }
          ]
        }
      ]
    }
  ],
  links: [
    {
      title: "AI Today 官网",
      description: "获取最新AI资讯和深度分析",
      url: "https://ai-today.com"
    },
    {
      title: "OpenAI 开发者文档",
      description: "GPT-4 API 使用指南和最佳实践",
      url: "https://platform.openai.com/docs"
    },
    {
      title: "Google AI 研究博客",
      description: "最新AI研究成果和技术洞察",
      url: "https://ai.googleblog.com"
    }
  ]
};

// 获取昨天的日期字符串 (YYYY-MM-DD 格式)
const getYesterday = (): string => {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  return yesterday.toISOString().split('T')[0];
};

// 格式化日期为显示用的字符串
const formatDateForDisplay = (dateStr: string): string => {
  const date = new Date(dateStr);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  });
};

function App() {
  const { 
    currentData, 
    isLoading, 
    error, 
    checkApiHealth,
    fetchTldrData 
  } = useAppStore();

  // 日期状态管理
  const [selectedDate, setSelectedDate] = useState<string>(getYesterday());
  const [showDatePicker, setShowDatePicker] = useState<boolean>(false);

  useEffect(() => {
    // 应用启动时初始化
    const initializeApp = async () => {
      await checkApiHealth();
      // 尝试获取选定日期的数据，如果失败则使用示例数据
      try {
        await fetchTldrData(selectedDate);
      } catch (err) {
        console.log('使用示例数据作为后备');
      }
    };

    initializeApp();
  }, [checkApiHealth, fetchTldrData, selectedDate]);

  // 处理日期变更
  const handleDateChange = async (newDate: string) => {
    setSelectedDate(newDate);
    setShowDatePicker(false);
    
    try {
      await fetchTldrData(newDate);
    } catch (err) {
      console.log('获取指定日期数据失败，使用示例数据');
    }
  };

  // 使用当前数据或示例数据
  const displayData = currentData || exampleData;

  return (
    <>
      <ParticleBackground />
      <DatePicker
        selectedDate={selectedDate}
        onDateChange={handleDateChange}
        show={showDatePicker}
        onToggle={() => setShowDatePicker(!showDatePicker)}
      />
      <CyberpunkLayout 
        isLoading={isLoading}
        loadingText="LOADING AI INTELLIGENCE..."
        keywords={displayData.keywords}
      >
        {error && (
          <div style={{ 
            background: 'rgba(255, 0, 0, 0.1)', 
            border: '1px solid #ff0000',
            borderRadius: '4px',
            padding: '10px',
            margin: '10px 0',
            color: '#ff0000',
            fontSize: '14px'
          }}>
            错误: {error.message}
          </div>
        )}
        

        
        <DataDisplay
          summary={displayData.summary}
          analysis={displayData.analysis}
          keywords={displayData.keywords}
          articles={displayData.articles}
          sections={displayData.sections}
          links={displayData.links}
          references={displayData.references}
        />
      </CyberpunkLayout>
    </>
  );
}

export default App;
