import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { ApiManager, type TldrResponse, type ApiError } from '../services/apiManager';

// 应用状态接口
interface AppState {
  // 数据状态
  currentData: TldrResponse | null;
  isLoading: boolean;
  error: ApiError | null;
  
  // 期刊相关
  selectedIssue: string | null;
  availableIssues: string[];
  
  // 历史记录
  dataHistory: Array<{
    issue: string;
    data: TldrResponse;
    timestamp: number;
  }>;
  
  // API 状态
  isApiHealthy: boolean;
  lastUpdateTime: number | null;
  
  // Actions
  setLoading: (loading: boolean) => void;
  setError: (error: ApiError | null) => void;
  setCurrentData: (data: TldrResponse | null) => void;
  setSelectedIssue: (issue: string | null) => void;
  setAvailableIssues: (issues: string[]) => void;
  addToHistory: (issue: string, data: TldrResponse) => void;
  clearHistory: () => void;
  setApiHealth: (healthy: boolean) => void;
  
  // 异步操作
  fetchTldrData: (dateOrIssue?: string) => Promise<void>;
  fetchAvailableIssues: () => Promise<void>;
  checkApiHealth: () => Promise<void>;
  refreshData: () => Promise<void>;
}

// 创建状态存储
export const useAppStore = create<AppState>()(
  persist(
    (set, get) => ({
      // 初始状态
      currentData: null,
      isLoading: false,
      error: null,
      selectedIssue: null,
      availableIssues: [],
      dataHistory: [],
      isApiHealthy: false,
      lastUpdateTime: null,

      // 基础 Actions
      setLoading: (loading) => set({ isLoading: loading }),
      
      setError: (error) => set({ error }),
      
      setCurrentData: (data) => set({ 
        currentData: data,
        lastUpdateTime: data ? Date.now() : null 
      }),
      
      setSelectedIssue: (issue) => set({ selectedIssue: issue }),
      
      setAvailableIssues: (issues) => set({ availableIssues: issues }),
      
      addToHistory: (issue, data) => {
        const { dataHistory } = get();
        const newEntry = {
          issue,
          data,
          timestamp: Date.now(),
        };
        
        // 避免重复记录，保持最新的10条记录
        const filteredHistory = dataHistory.filter(item => item.issue !== issue);
        const newHistory = [newEntry, ...filteredHistory].slice(0, 10);
        
        set({ dataHistory: newHistory });
      },
      
      clearHistory: () => set({ dataHistory: [] }),
      
      setApiHealth: (healthy) => set({ isApiHealthy: healthy }),

      // 异步操作
      fetchTldrData: async (dateOrIssue) => {
        const { setLoading, setError, setCurrentData, addToHistory } = get();
        
        try {
          setLoading(true);
          setError(null);
          
          const data = await ApiManager.getTldrData(dateOrIssue);
          
          // 如果传入的是日期格式，尝试获取对应的 Markdown 内容
          if (dateOrIssue && /^\d{4}-\d{2}-\d{2}$/.test(dateOrIssue)) {
            try {
              const markdownResult = await ApiManager.getSchedulerMarkdown(dateOrIssue);
              
              if (markdownResult.success && markdownResult.content) {
                console.log('[Store] 成功获取 Markdown 内容，准备解析并合并');
                
                // 解析 Markdown 提取新闻条目
                const parseMarkdownNews = (mdContent: string) => {
                  const articles = [];
                  
                  // 匹配格式：数字. **标题｜英文标题**
                  // 然后提取来源和链接
                  const newsPattern = /\d+\.\s+\*\*(.+?)\*\*\s+来源：(.+?)｜(.+?)\s+链接：(https?:\/\/[^\s]+)/g;
                  
                  let match;
                  while ((match = newsPattern.exec(mdContent)) !== null) {
                    const [, title, source, time, url] = match;
                    
                    // 提取中文标题（｜之前的部分）
                    const chineseTitle = title.split('｜')[0].trim();
                    
                    articles.push({
                      title: chineseTitle,
                      content: `来源：${source} | ${time}`,
                      links: [{
                        url: url,
                        text: '查看原文'
                      }],
                      word_count: chineseTitle.length
                    });
                  }
                  
                  return articles;
                };
                
                const newsArticles = parseMarkdownNews(markdownResult.content);
                
                if (newsArticles.length > 0) {
                  console.log(`[Store] 解析出 ${newsArticles.length} 条新闻`);
                  
                  // 查找或创建"其他资讯" section
                  const existingSections = data.sections || [];
                  let miscSection = existingSections.find(
                    s => s.title === 'Miscellaneous' || s.title === '其他资讯'
                  );
                  
                  if (miscSection) {
                    // 如果已存在，将 Markdown 新闻放在最前面
                    miscSection.articles = [...newsArticles, ...(miscSection.articles || [])];
                    miscSection.article_count = miscSection.articles.length;
                  } else {
                    // 如果不存在，创建新的 section
                    const newSection = {
                      title: '其他资讯',
                      articles: newsArticles,
                      article_count: newsArticles.length
                    };
                    data.sections = [...existingSections, newSection];
                  }
                  
                  console.log('[Store] Markdown 新闻已合并到"其他资讯"顶部');
                } else {
                  console.log('[Store] 未能解析出新闻条目');
                }
              } else {
                console.log('[Store] 未找到对应日期的 Markdown 内容，使用原始数据');
              }
            } catch (mdError) {
              console.warn('[Store] 获取 Markdown 内容失败，继续使用原始数据:', mdError);
              // 不中断主流程，继续使用原始数据
            }
          }
          
          setCurrentData(data);
          
          // 添加到历史记录（只对非日期格式的issue添加）
          if (dateOrIssue && !/^\d{4}-\d{2}-\d{2}$/.test(dateOrIssue)) {
            addToHistory(dateOrIssue, data);
          }
          
        } catch (error) {
          console.error('[Store] 获取数据失败:', error);
          setError(error as ApiError);
        } finally {
          setLoading(false);
        }
      },

      fetchAvailableIssues: async () => {
        const { setError, setAvailableIssues } = get();
        
        try {
          const issues = await ApiManager.getAvailableIssues();
          setAvailableIssues(issues);
        } catch (error) {
          console.error('[Store] 获取期刊列表失败:', error);
          setError(error as ApiError);
        }
      },

      checkApiHealth: async () => {
        const { setApiHealth } = get();
        
        try {
          const healthy = await ApiManager.checkHealth();
          setApiHealth(healthy);
        } catch (error) {
          console.error('[Store] API健康检查失败:', error);
          setApiHealth(false);
        }
      },

      refreshData: async () => {
        const { selectedIssue, fetchTldrData } = get();
        await fetchTldrData(selectedIssue || undefined);
      },
    }),
    {
      name: 'ai-today-app-store',
      // 只持久化部分状态
      partialize: (state) => ({
        selectedIssue: state.selectedIssue,
        dataHistory: state.dataHistory,
        availableIssues: state.availableIssues,
      }),
    }
  )
);

// 导出类型
export type { AppState };