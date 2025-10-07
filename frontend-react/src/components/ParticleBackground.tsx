import React, { useEffect, useRef } from 'react';
import styled from 'styled-components';

const ParticleContainer = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
`;

const Canvas = styled.canvas`
  width: 100%;
  height: 100%;
`;

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  color: string;
  opacity: number;
  life: number;
  maxLife: number;
}

const ParticleBackground: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const particlesRef = useRef<Particle[]>([]);
  const animationRef = useRef<number>(0);

  const colors = ['#00ffff', '#ff00ff', '#00ff00', '#0080ff', '#8000ff'];

  const createParticle = (canvas: HTMLCanvasElement): Particle => {
    return {
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.5,
      vy: (Math.random() - 0.5) * 0.5,
      size: Math.random() * 2 + 1,
      color: colors[Math.floor(Math.random() * colors.length)],
      opacity: Math.random() * 0.5 + 0.2,
      life: 0,
      maxLife: Math.random() * 200 + 100
    };
  };

  const updateParticle = (particle: Particle, canvas: HTMLCanvasElement) => {
    particle.x += particle.vx;
    particle.y += particle.vy;
    particle.life++;

    // 边界检测
    if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1;
    if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1;

    // 生命周期透明度变化
    const lifeRatio = particle.life / particle.maxLife;
    particle.opacity = Math.sin(lifeRatio * Math.PI) * 0.5 + 0.2;

    return particle.life < particle.maxLife;
  };

  const drawParticle = (ctx: CanvasRenderingContext2D, particle: Particle) => {
    ctx.save();
    ctx.globalAlpha = particle.opacity;
    ctx.fillStyle = particle.color;
    ctx.shadowBlur = 10;
    ctx.shadowColor = particle.color;
    
    ctx.beginPath();
    ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
    ctx.fill();
    
    ctx.restore();
  };

  const drawConnections = (ctx: CanvasRenderingContext2D, particles: Particle[]) => {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 100) {
          ctx.save();
          ctx.globalAlpha = (1 - distance / 100) * 0.2;
          ctx.strokeStyle = '#00ffff';
          ctx.lineWidth = 0.5;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
          ctx.restore();
        }
      }
    }
  };

  const animate = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // 清除画布
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 更新粒子
    particlesRef.current = particlesRef.current.filter(particle => 
      updateParticle(particle, canvas)
    );

    // 添加新粒子
    while (particlesRef.current.length < 50) {
      particlesRef.current.push(createParticle(canvas));
    }

    // 绘制连接线
    drawConnections(ctx, particlesRef.current);

    // 绘制粒子
    particlesRef.current.forEach(particle => {
      drawParticle(ctx, particle);
    });

    animationRef.current = requestAnimationFrame(animate);
  };

  const resizeCanvas = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    resizeCanvas();
    
    // 初始化粒子
    for (let i = 0; i < 50; i++) {
      particlesRef.current.push(createParticle(canvas));
    }

    animate();

    const handleResize = () => {
      resizeCanvas();
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, []);

  return (
    <ParticleContainer>
      <Canvas ref={canvasRef} />
    </ParticleContainer>
  );
};

export default ParticleBackground;