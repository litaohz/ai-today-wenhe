import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { Lunar, Solar } from 'lunar-javascript';

const LayoutContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
`;

const Header = styled(motion.header)`
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--neon-cyan);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
  padding: 1rem 2rem;
  position: sticky;
  top: 0;
  z-index: 100;
`;

const HeaderContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Logo = styled(motion.h1)`
  font-family: 'Orbitron', monospace;
  font-size: 2rem;
  font-weight: 900;
  color: var(--neon-cyan);
  text-shadow: var(--text-glow);
  margin: 0;
  
  &::before {
    content: '◢';
    margin-right: 0.5rem;
    color: var(--neon-pink);
  }
  
  &::after {
    content: '◣';
    margin-left: 0.5rem;
    color: var(--neon-green);
  }
`;

const DateTimeContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
  font-family: 'Orbitron', monospace;
  
  @media (max-width: 768px) {
    align-items: center;
  }
`;

const LunarDate = styled(motion.div)`
  font-size: 0.8rem;
  color: var(--neon-pink);
  text-shadow: 0 0 5px var(--neon-pink);
  opacity: 0.8;
`;

const FloatingKeywords = styled.div`
  position: absolute;
  top: 50%;
  left: 40%;
  transform: translateY(-50%);
  display: flex;
  flex-wrap: wrap;
  gap: 12px 16px;
  max-width: 25%;
  z-index: 2;
  align-items: flex-start;
  align-content: center;

  @media (max-width: 1024px) {
    left: 52%;
    max-width: 50%;
    gap: 8px 12px;
  }

  @media (max-width: 768px) {
    left: 50%;
    max-width: 45%;
    gap: 6px 10px;
  }

  @media (max-width: 480px) {
    left: 50%;
    max-width: 40%;
    gap: 4px 8px;
  }
`;

const FloatingKeyword = styled(motion.span)`
  background: linear-gradient(135deg, var(--neon-cyan), var(--neon-pink));
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 0.9rem;
  font-weight: 600;
  text-shadow: 0 0 10px var(--neon-cyan);
  word-break: break-word;
  line-height: 1.4;
  
  @media (max-width: 768px) {
    font-size: 0.8rem;
  }
`;

const Clock = styled(motion.div)`
  font-family: 'Orbitron', monospace;
  font-size: 1.2rem;
  color: var(--neon-green);
  text-shadow: var(--text-glow);
  
  @media (max-width: 768px) {
    font-size: 1rem;
  }
`;

const MainContent = styled.main`
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  width: 100%;
`;

const LoadingOverlay = styled(motion.div)`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const LoadingText = styled(motion.div)`
  font-family: 'Orbitron', monospace;
  font-size: 1.5rem;
  color: var(--neon-cyan);
  text-shadow: var(--text-glow);
  margin-bottom: 2rem;
`;

const LoadingBar = styled.div`
  width: 300px;
  height: 4px;
  background: rgba(0, 255, 255, 0.2);
  border-radius: 2px;
  overflow: hidden;
  position: relative;
`;

const LoadingProgress = styled(motion.div)`
  height: 100%;
  background: linear-gradient(90deg, var(--neon-cyan), var(--neon-pink));
  border-radius: 2px;
  box-shadow: 0 0 10px var(--neon-cyan);
`;

interface CyberpunkLayoutProps {
  children: React.ReactNode;
  keywords?: string[];
  isLoading?: boolean;
  loadingText?: string;
}

const CyberpunkLayout: React.FC<CyberpunkLayoutProps> = ({ 
  children, 
  keywords = [],
  isLoading = false, 
  loadingText = "正在加载..." 
}) => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [lunarDate, setLunarDate] = useState('');
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);

  useEffect(() => {
    const updateDateTime = () => {
      const now = new Date();
      setCurrentTime(now);
      
      // 计算农历日期
      const solar = Solar.fromDate(now);
      const lunar = solar.getLunar();
      const lunarStr = `${lunar.getYearInChinese()}年${lunar.getMonthInChinese()}月${lunar.getDayInChinese()}`;
      setLunarDate(lunarStr);
    };

    updateDateTime();
     const timer = setInterval(updateDateTime, 1000);
     return () => clearInterval(timer);
   }, []);

   useEffect(() => {
     const handleResize = () => {
       setWindowWidth(window.innerWidth);
     };

     window.addEventListener('resize', handleResize);
     return () => window.removeEventListener('resize', handleResize);
   }, []);

   // 根据屏幕宽度决定显示的关键词数量
   const getMaxKeywords = () => {
     if (windowWidth < 480) return 4;
     if (windowWidth < 768) return 6;
     if (windowWidth < 1024) return 8;
     return 10;
   };

   const displayKeywords = keywords.slice(0, getMaxKeywords());

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', { 
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <LayoutContainer>
      {isLoading && (
        <LoadingOverlay
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <LoadingText
            animate={{ 
              textShadow: [
                '0 0 10px #00ffff',
                '0 0 20px #00ffff',
                '0 0 10px #00ffff'
              ]
            }}
            transition={{ duration: 1.5, repeat: Infinity }}
          >
            {loadingText}
          </LoadingText>
          <LoadingBar>
            <LoadingProgress
              initial={{ width: 0 }}
              animate={{ width: '100%' }}
              transition={{ duration: 2, ease: 'easeInOut' }}
            />
          </LoadingBar>
        </LoadingOverlay>
      )}

      <Header
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, ease: 'easeOut' }}
      >
        <HeaderContent>
          <Logo
            whileHover={{ scale: 1.05 }}
            transition={{ type: 'spring', stiffness: 300 }}
          >
            AI TODAY
          </Logo>

          <FloatingKeywords>
            {displayKeywords.map((keyword, index) => (
              <FloatingKeyword
                key={keyword}
                initial={{ opacity: 0, y: 20 }}
                animate={{ 
                  opacity: 1, 
                  y: 0,
                  x: [0, Math.sin(index * 0.5) * 10, 0]
                }}
                transition={{ 
                  duration: 0.8, 
                  delay: index * 0.1,
                  x: { duration: 3 + index * 0.5, repeat: Infinity, ease: "easeInOut" }
                }}
                whileHover={{ scale: 1.1 }}
              >
                {keyword}
              </FloatingKeyword>
            ))}
          </FloatingKeywords>

          <DateTimeContainer>
            <Clock
              animate={{ 
                textShadow: [
                  '0 0 5px #00ff00',
                  '0 0 15px #00ff00',
                  '0 0 5px #00ff00'
                ]
              }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              {formatTime(currentTime)}
            </Clock>
            <LunarDate
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              {lunarDate}
            </LunarDate>
          </DateTimeContainer>
        </HeaderContent>
      </Header>

      <MainContent>
        {children}
      </MainContent>
    </LayoutContainer>
  );
};

export default CyberpunkLayout;