import axios from 'axios';

// 数据类型定义
export interface ArticleLink {
  url: string;
  text: string;
}

export interface Article {
  title: string;
  content: string;
  links: ArticleLink[];
  word_count: number;
}

export interface Section {
  title: string;
  articles: Article[];
  article_count: number;
}

export interface ExternalLink {
  title: string;
  description: string;
  url: string;
}

export interface Reference {
  id: number;
  title: string;
  content: string;
  section: string;
  links: ArticleLink[];
}

export interface TldrResponse {
  url: string;
  title: string;
  subtitle: string;
  content: string;
  meta_description: string;
  articles: Article[];
  sections?: Section[];
  word_count?: number;
  article_count?: number;
  crawled_at?: string;
  database_id?: number;
  processing_status?: string;
  summary?: string;
  analysis?: string;
  keywords?: string[];
  ai_processed?: boolean;
  processing_timestamp?: number;
  references?: Reference[];
}

export interface ApiError {
  message: string;
  status?: number;
}

// API 基础配置
const API_BASE_URL = 'http://localhost:8000/api/v1';

// 创建 axios 实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    console.log(`[API] 请求: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API] 请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    console.log(`[API] 响应: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('[API] 响应错误:', error.response?.status, error.message);
    return Promise.reject(error);
  }
);

// API 管理器类
export class ApiManager {
  // 获取 TLDR 数据
  static async getTldrData(dateOrIssue?: string): Promise<TldrResponse> {
    try {
      const params: any = {};
      
      // 如果参数是日期格式 (YYYY-MM-DD)，构建对应的URL
      if (dateOrIssue && /^\d{4}-\d{2}-\d{2}$/.test(dateOrIssue)) {
        params.url = `https://tldr.tech/ai/${dateOrIssue}`;
      } else if (dateOrIssue) {
        // 否则作为issue参数处理
        params.issue = dateOrIssue;
      }
      
      const response = await apiClient.get('/tldr', { params });
      
      // 后端返回的是包装对象 { success, data, error, cached, processing_time }
      // 我们需要提取其中的 data 字段
      const responseData = response.data;
      
      if (!responseData.success) {
        throw new Error(responseData.error || '获取数据失败');
      }
      
      // 返回实际的数据内容
      return responseData.data;
    } catch (error) {
      console.error('[ApiManager] 获取 TLDR 数据失败:', error);
      throw this.handleError(error);
    }
  }

  // 获取可用期刊列表
  static async getAvailableIssues(): Promise<string[]> {
    try {
      const response = await apiClient.get('/issues');
      return response.data.issues || [];
    } catch (error) {
      console.error('[ApiManager] 获取期刊列表失败:', error);
      throw this.handleError(error);
    }
  }

  // 检查 API 健康状态
  static async checkHealth(): Promise<boolean> {
    try {
      const response = await apiClient.get('/health');
      return response.status === 200;
    } catch (error) {
      console.error('[ApiManager] 健康检查失败:', error);
      return false;
    }
  }

  // 错误处理
  private static handleError(error: any): ApiError {
    if (axios.isAxiosError(error)) {
      return {
        message: error.response?.data?.message || error.message || '网络请求失败',
        status: error.response?.status,
      };
    }
    return {
      message: error.message || '未知错误',
    };
  }
}

// 导出默认实例
export default ApiManager;