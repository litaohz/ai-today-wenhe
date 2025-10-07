import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { useAppStore } from '../store/appStore';

const SelectorContainer = styled(motion.div)`
  background: rgba(0, 20, 40, 0.9);
  border: 1px solid #00ffff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
`;

const SelectorTitle = styled.h3`
  color: #00ffff;
  font-size: 18px;
  margin-bottom: 15px;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-shadow: 0 0 10px #00ffff;
`;

const SelectWrapper = styled.div`
  position: relative;
  margin-bottom: 15px;
`;

const CustomSelect = styled.select`
  width: 100%;
  background: rgba(0, 10, 20, 0.8);
  border: 1px solid #00ffff;
  border-radius: 4px;
  color: #00ffff;
  padding: 12px 16px;
  font-size: 14px;
  font-family: 'Courier New', monospace;
  cursor: pointer;
  transition: all 0.3s ease;

  &:focus {
    outline: none;
    border-color: #ff00ff;
    box-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
  }

  &:hover {
    border-color: #ff00ff;
  }

  option {
    background: rgba(0, 10, 20, 0.95);
    color: #00ffff;
    padding: 8px;
  }
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
`;

const ActionButton = styled(motion.button)<{ variant?: 'primary' | 'secondary' | 'danger' }>`
  background: ${props => {
    switch (props.variant) {
      case 'primary': return 'linear-gradient(45deg, #00ffff, #0080ff)';
      case 'danger': return 'linear-gradient(45deg, #ff0080, #ff0040)';
      default: return 'linear-gradient(45deg, #404040, #606060)';
    }
  }};
  border: none;
  border-radius: 4px;
  color: white;
  padding: 10px 16px;
  font-size: 12px;
  font-family: 'Courier New', monospace;
  text-transform: uppercase;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 255, 255, 0.4);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
`;

const StatusIndicator = styled.div<{ status: 'online' | 'offline' | 'loading' }>`
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: ${props => {
    switch (props.status) {
      case 'online': return '#00ff00';
      case 'offline': return '#ff0000';
      default: return '#ffff00';
    }
  }};

  &::before {
    content: '';
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: currentColor;
    animation: ${props => props.status === 'loading' ? 'pulse 1.5s infinite' : 'none'};
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }
`;

const HistoryList = styled.div`
  margin-top: 15px;
  max-height: 200px;
  overflow-y: auto;
`;

const HistoryItem = styled(motion.div)`
  background: rgba(0, 10, 20, 0.6);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 4px;
  padding: 8px 12px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;

  &:hover {
    border-color: #00ffff;
    background: rgba(0, 20, 40, 0.8);
  }

  .issue-name {
    color: #00ffff;
    font-weight: bold;
  }

  .timestamp {
    color: #888;
    font-size: 10px;
  }
`;

const IssueSelector: React.FC = () => {
  const {
    selectedIssue,
    availableIssues,
    isLoading,
    isApiHealthy,
    dataHistory,
    setSelectedIssue,
    fetchTldrData,
    fetchAvailableIssues,
    checkApiHealth,
    clearHistory,
  } = useAppStore();

  const [localSelectedIssue, setLocalSelectedIssue] = useState(selectedIssue || '');

  useEffect(() => {
    // 初始化时检查API健康状态和获取期刊列表
    checkApiHealth();
    fetchAvailableIssues();
  }, [checkApiHealth, fetchAvailableIssues]);

  const handleIssueChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const value = event.target.value;
    setLocalSelectedIssue(value);
    setSelectedIssue(value || null);
  };

  const handleFetchData = async () => {
    if (localSelectedIssue) {
      await fetchTldrData(localSelectedIssue);
    } else {
      await fetchTldrData();
    }
  };

  const handleHistoryItemClick = async (issue: string) => {
    setLocalSelectedIssue(issue);
    setSelectedIssue(issue);
    await fetchTldrData(issue);
  };

  const formatTimestamp = (timestamp: number) => {
    return new Date(timestamp).toLocaleString('zh-CN', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getApiStatus = () => {
    if (isLoading) return 'loading';
    return isApiHealthy ? 'online' : 'offline';
  };

  const getStatusText = () => {
    if (isLoading) return 'LOADING...';
    return isApiHealthy ? 'API ONLINE' : 'API OFFLINE';
  };

  return (
    <SelectorContainer
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <SelectorTitle>AI Today Control Panel</SelectorTitle>
      
      <StatusIndicator status={getApiStatus()}>
        {getStatusText()}
      </StatusIndicator>

      <SelectWrapper>
        <CustomSelect
          value={localSelectedIssue}
          onChange={handleIssueChange}
          disabled={isLoading}
        >
          <option value="">选择期刊 (最新)</option>
          {availableIssues.map((issue) => (
            <option key={issue} value={issue}>
              {issue}
            </option>
          ))}
        </CustomSelect>
      </SelectWrapper>

      <ButtonGroup>
        <ActionButton
          variant="primary"
          onClick={handleFetchData}
          disabled={isLoading}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {isLoading ? 'LOADING...' : 'FETCH DATA'}
        </ActionButton>

        <ActionButton
          variant="secondary"
          onClick={fetchAvailableIssues}
          disabled={isLoading}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          REFRESH ISSUES
        </ActionButton>

        <ActionButton
          variant="secondary"
          onClick={checkApiHealth}
          disabled={isLoading}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          CHECK API
        </ActionButton>

        {dataHistory.length > 0 && (
          <ActionButton
            variant="danger"
            onClick={clearHistory}
            disabled={isLoading}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            CLEAR HISTORY
          </ActionButton>
        )}
      </ButtonGroup>

      {dataHistory.length > 0 && (
        <HistoryList>
          <SelectorTitle style={{ fontSize: '14px', marginBottom: '10px' }}>
            Recent History
          </SelectorTitle>
          <AnimatePresence>
            {dataHistory.map((item, index) => (
              <HistoryItem
                key={`${item.issue}-${item.timestamp}`}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ delay: index * 0.1 }}
                onClick={() => handleHistoryItemClick(item.issue)}
              >
                <span className="issue-name">{item.issue}</span>
                <span className="timestamp">{formatTimestamp(item.timestamp)}</span>
              </HistoryItem>
            ))}
          </AnimatePresence>
        </HistoryList>
      )}
    </SelectorContainer>
  );
};

export default IssueSelector;