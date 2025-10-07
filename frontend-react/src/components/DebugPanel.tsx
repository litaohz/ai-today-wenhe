import React, { useState } from 'react';
import styled from 'styled-components';
import { ApiManager } from '../services/apiManager';

const DebugContainer = styled.div`
  position: fixed;
  top: 20px;
  right: 20px;
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid #00ff00;
  border-radius: 8px;
  padding: 16px;
  color: #00ff00;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  z-index: 1000;
  min-width: 300px;
`;

const DebugButton = styled.button`
  background: #001100;
  border: 1px solid #00ff00;
  color: #00ff00;
  padding: 8px 16px;
  margin: 4px;
  border-radius: 4px;
  cursor: pointer;
  font-family: 'Courier New', monospace;
  
  &:hover {
    background: #002200;
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const DebugOutput = styled.pre`
  background: #000;
  border: 1px solid #333;
  padding: 8px;
  margin: 8px 0;
  border-radius: 4px;
  max-height: 200px;
  overflow-y: auto;
  font-size: 10px;
`;

const DebugPanel: React.FC = () => {
  const [output, setOutput] = useState<string>('Debug Panel Ready...');
  const [isLoading, setIsLoading] = useState(false);

  const log = (message: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setOutput(prev => `${prev}\n[${timestamp}] ${message}`);
  };

  const testHealthCheck = async () => {
    setIsLoading(true);
    log('开始健康检查测试...');
    
    try {
      // 直接使用fetch测试
      log('使用fetch直接测试...');
      const response = await fetch('http://localhost:8000/api/v1/health', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      log(`Fetch响应状态: ${response.status}`);
      
      if (response.ok) {
        const data = await response.json();
        log(`Fetch成功: ${JSON.stringify(data, null, 2)}`);
      } else {
        log(`Fetch失败: ${response.statusText}`);
      }
      
      // 使用ApiManager测试
      log('使用ApiManager测试...');
      const healthy = await ApiManager.checkHealth();
      log(`ApiManager结果: ${healthy}`);
      
    } catch (error) {
      log(`错误: ${error}`);
    } finally {
      setIsLoading(false);
    }
  };

  const testTldrData = async () => {
    setIsLoading(true);
    log('开始TLDR数据测试...');
    
    try {
      const data = await ApiManager.getTldrData();
      log(`TLDR数据获取成功: ${JSON.stringify(data, null, 2).substring(0, 200)}...`);
    } catch (error) {
      log(`TLDR数据获取失败: ${error}`);
    } finally {
      setIsLoading(false);
    }
  };

  const clearOutput = () => {
    setOutput('Debug Panel Ready...');
  };

  return (
    <DebugContainer>
      <h4>🔧 Debug Panel</h4>
      <div>
        <DebugButton onClick={testHealthCheck} disabled={isLoading}>
          Test Health Check
        </DebugButton>
        <DebugButton onClick={testTldrData} disabled={isLoading}>
          Test TLDR Data
        </DebugButton>
        <DebugButton onClick={clearOutput}>
          Clear
        </DebugButton>
      </div>
      <DebugOutput>{output}</DebugOutput>
    </DebugContainer>
  );
};

export default DebugPanel;