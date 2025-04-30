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
    const totalLines = 150;
    const spiralSpeed = 0.5;
    const maxTime = 5500; // 5 seconds of animation
    let angle = 0;
    const lines = [];
    let welcomeAlpha = 0;
    let welcomeTimer = 0;

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
        ctx.strokeStyle = `rgba(255, 105, 180, ${line.alpha})`;
        ctx.lineWidth = 1.5;
        ctx.shadowBlur = 10;
        ctx.shadowColor = 'hotpink';
        ctx.stroke();
      }

      // Fade in text
      if (lines.length >= totalLines) {
        if (welcomeTimer < 60) {
          welcomeTimer++;
          welcomeAlpha = welcomeTimer / 60;
        }

        ctx.font = 'bold 60px Arial';
        ctx.fillStyle = `rgba(255, 182, 193, ${welcomeAlpha})`;
        ctx.textAlign = 'center';
        // Move the "WELCOME" text slightly lower (by adjusting the Y position)
        const textYPosition = centerY + 23;  // Adjust this value to move lower or higher
        ctx.fillText('WELCOME', centerX, textYPosition);
      }

      // Stop drawing after the animation is done
      if (welcomeTimer >= 120) {
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

