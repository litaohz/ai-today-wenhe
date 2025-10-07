import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';

interface DatePickerProps {
  selectedDate: string;
  onDateChange: (date: string) => void;
  show: boolean;
  onToggle: () => void;
}

const DatePickerContainer = styled.div`
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
`;

const DateButton = styled(motion.button)`
  background: linear-gradient(135deg, var(--neon-cyan), var(--neon-pink));
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  color: var(--bg-primary);
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
  transition: all 0.3s ease;

  &:hover {
    box-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
    transform: translateY(-2px);
  }

  @media (max-width: 768px) {
    font-size: 0.8rem;
    padding: 6px 12px;
  }
`;

const DatePickerPanel = styled(motion.div)`
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: rgba(0, 20, 40, 0.95);
  border: 1px solid var(--neon-cyan);
  border-radius: 12px;
  padding: 16px;
  min-width: 280px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);

  @media (max-width: 768px) {
    min-width: 240px;
    padding: 12px;
  }
`;

const DateInput = styled.input`
  width: 100%;
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid var(--neon-cyan);
  border-radius: 6px;
  padding: 8px 12px;
  color: var(--text-primary);
  font-size: 0.9rem;
  margin-bottom: 12px;

  &:focus {
    outline: none;
    border-color: var(--neon-pink);
    box-shadow: 0 0 10px rgba(255, 20, 147, 0.3);
  }

  &::-webkit-calendar-picker-indicator {
    filter: invert(1);
    cursor: pointer;
  }
`;

const QuickDateList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 6px;
`;

const QuickDateButton = styled(motion.button)`
  background: transparent;
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 6px;
  padding: 8px 12px;
  color: var(--text-secondary);
  font-size: 0.85rem;
  cursor: pointer;
  text-align: left;
  transition: all 0.3s ease;

  &:hover {
    background: rgba(0, 255, 255, 0.1);
    border-color: var(--neon-cyan);
    color: var(--text-primary);
  }

  &.selected {
    background: rgba(0, 255, 255, 0.2);
    border-color: var(--neon-cyan);
    color: var(--neon-cyan);
  }
`;

const SectionTitle = styled.h4`
  color: var(--neon-green);
  font-size: 0.8rem;
  margin: 0 0 8px 0;
  text-transform: uppercase;
  letter-spacing: 1px;
`;

const DatePicker: React.FC<DatePickerProps> = ({
  selectedDate,
  onDateChange,
  show,
  onToggle
}) => {
  const [inputDate, setInputDate] = useState(selectedDate);
  const containerRef = useRef<HTMLDivElement>(null);

  // 生成快速选择日期
  const getQuickDates = () => {
    const dates = [];
    const today = new Date();
    
    for (let i = 1; i <= 7; i++) {
      const date = new Date(today);
      date.setDate(today.getDate() - i);
      const dateStr = date.toISOString().split('T')[0];
      const displayName = i === 1 ? '当前' : 
                         i === 2 ? '前天' : 
                         `${i}天前`;
      dates.push({
        value: dateStr,
        label: displayName,
        fullDate: date.toLocaleDateString('zh-CN', {
          month: 'short',
          day: 'numeric',
          weekday: 'short'
        })
      });
    }
    return dates;
  };

  const quickDates = getQuickDates();

  // 格式化显示日期
  const formatDisplayDate = (dateStr: string) => {
    const date = new Date(dateStr);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);

    if (dateStr === today.toISOString().split('T')[0]) {
      return '今天';
    } else if (dateStr === yesterday.toISOString().split('T')[0]) {
      return '当前';
    } else {
      return date.toLocaleDateString('zh-CN', {
        month: 'short',
        day: 'numeric'
      });
    }
  };

  // 点击外部关闭
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        if (show) {
          onToggle();
        }
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [show, onToggle]);

  // 同步输入框值
  useEffect(() => {
    setInputDate(selectedDate);
  }, [selectedDate]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputDate(e.target.value);
  };

  const handleInputSubmit = () => {
    if (inputDate && inputDate !== selectedDate) {
      onDateChange(inputDate);
    }
  };

  const handleQuickDateSelect = (date: string) => {
    onDateChange(date);
  };

  return (
    <DatePickerContainer ref={containerRef}>
      <DateButton
        onClick={onToggle}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        📅 {formatDisplayDate(selectedDate)}
      </DateButton>

      <AnimatePresence>
        {show && (
          <DatePickerPanel
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            transition={{ duration: 0.2 }}
          >
            <SectionTitle>选择日期</SectionTitle>
            <DateInput
              type="date"
              value={inputDate}
              onChange={handleInputChange}
              onBlur={handleInputSubmit}
              onKeyPress={(e) => e.key === 'Enter' && handleInputSubmit()}
              max={new Date().toISOString().split('T')[0]}
            />

            <SectionTitle>快速选择</SectionTitle>
            <QuickDateList>
              {quickDates.map((date) => (
                <QuickDateButton
                  key={date.value}
                  onClick={() => handleQuickDateSelect(date.value)}
                  className={selectedDate === date.value ? 'selected' : ''}
                  whileHover={{ x: 4 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>{date.label}</span>
                    <span style={{ opacity: 0.7 }}>{date.fullDate}</span>
                  </div>
                </QuickDateButton>
              ))}
            </QuickDateList>
          </DatePickerPanel>
        )}
      </AnimatePresence>
    </DatePickerContainer>
  );
};

export default DatePicker;