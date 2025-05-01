import { useEffect, useRef } from 'react';

const SpiralIntro = ({ onFinish }) => {
  const canvasRef = useRef(null);
  const animationFrameId = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const width = canvas.width = window.innerWidth;
    const height = canvas.height = window.innerHeight;
    const centerX = width / 2;
    const centerY = height / 2;

    const maxRadius = Math.min(width, height) * 1.05;
    const totalLines = 199.5;
    const spiralSpeed = .15;
    let angle = 0;
    const lines = [];
    let welcomeAlpha = 0;
    let welcomeTimer = 0;
    const fadeInDuration = 200; // Time to fade in
    const textRiseOffset = 250; // Amount to rise the text
    let holdTimer = 0; // Timer to hold the text
    const holdDuration = 60; // 240 frames = 4 seconds at 60 FPS
    const textDelayFrames = 1; // 2 seconds at 60fps
    let textDelayTimer = 0;

    function generateNextLine() {
      const x1 = centerX + Math.cos(angle) * maxRadius;
      const y1 = centerY + Math.sin(angle) * maxRadius;
      const x2 = centerX;
      const y2 = centerY;

      lines.push({ x1, y1, x2, y2, alpha: 0 });
      angle += spiralSpeed;
    }

    
    
    
    function draw() {
      ctx.fillStyle = '#1c1c1c';
      ctx.fillRect(0, 0, width, height);

      if (lines.length < totalLines) generateNextLine();

      // Draw the spiral lines
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        if (line.alpha < 1) line.alpha += 0.05;

        ctx.beginPath();
        ctx.moveTo(line.x1, line.y1);
        ctx.lineTo(line.x2, line.y2);
        ctx.strokeStyle = `rgba(250,0, 138, ${line.alpha})`;
        ctx.lineWidth = 1.75;
        ctx.shadowBlur = 20;
        ctx.shadowColor = '#03fdf3';
        ctx.stroke();
      }

      // Wait before starting text animation
        if (textDelayTimer < textDelayFrames) {
          if (welcomeTimer < fadeInDuration) {
            welcomeTimer++;
          } else {
            holdTimer++;
          }


       // Easing for fade and rise
       const t = Math.min(welcomeTimer / fadeInDuration, 1);
       const easedT = (1 - Math.cos(t * Math.PI)) / 2; // smoother easing

       welcomeAlpha = easedT         
          const baseY = centerY + 22;
          const animatedY = baseY + textRiseOffset * (1 - easedT);
          const animatedYTop = baseY - textRiseOffset * (1 - easedT);
          
          ctx.font = 'bold 60px Arial';
          ctx.textAlign = 'center';
          // Set stroke style for outline
          ctx.lineWidth = 3;
          ctx.strokeStyle = `rgba(3, 253, 243, ${welcomeAlpha})`; // black outline with matching alpha
          ctx.strokeText('.ptdX editor', centerX, animatedY);
          ctx.strokeText('.ptdX editor', centerX, animatedYTop);
          ctx.fillStyle = `rgba(253,252, 3, ${welcomeAlpha})`;          
          ctx.fillText('.ptdX editor', centerX, animatedY);
          ctx.fillText('.ptdX editor', centerX, animatedYTop);
          
        }

        // End after fade + hold complete
      if (welcomeTimer >= fadeInDuration && holdTimer >= holdDuration) {
        cancelAnimationFrame(animationFrameId.current);
        onFinish?.();
      } else {
        animationFrameId.current = requestAnimationFrame(draw);
      }
      }

    // Start the animation
    draw();

    // Cleanup on component unmount
    return () => {
      cancelAnimationFrame(animationFrameId.current);
      ctx.clearRect(0, 0, width, height);
    };
  }, [onFinish]);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        zIndex: 9999,
        background: '#1c1c1c',
        pointerEvents: 'none', // Allow clicks to pass through the canvas
      }}
    />
  );
};

export default SpiralIntro;

