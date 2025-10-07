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