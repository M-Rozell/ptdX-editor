// src/components/SplashTempest.jsx
import { useEffect, useRef } from 'react';

export default function SplashTempest({ onFinish }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener('resize', resize);

    const centerX = () => canvas.width / 2;
    const centerY = () => canvas.height / 2;

    const spokes = 100;
    let time = 0;
    let animationId;

    
    
    
    function drawWeb() {
      ctx.strokeStyle = '#02fcf2';
      ctx.lineWidth = 1;

        const fov = 600; // Wider field of view (less aggressive shrink)
        const rings = 3;
        const ringsTwo = 50; // Number of rings
        const spokesTwo = 350; // Number of spokes
        const baseRadius = 350; // Increase size of web
        const depthSpacing = 300;
        const yOffset = -18; // Adjust vertical position of web

        for (let z = 1; z < rings; z++) {
            const scale = fov / (fov + z * depthSpacing);
            const radius = baseRadius * scale;
            
            // Calculate an angular offset for each ring
            const rotationOffset = z * 0.1; // Gradual angular shift for each deeper ring
            
            // Draw each ring's spokes
            for (let i = 0; i < spokes; i++) {
              const angle = (i / spokes) * Math.PI * .05 + rotationOffset + time * 0.01;
              
              const x = Math.cos(angle) * radius;
              const y = Math.sin(angle) * radius;
              
              const screenX = centerX() + x;
              const screenY = centerY() + y + yOffset;
              
              if (i === 0) {
                ctx.beginPath();
                ctx.moveTo(screenX, screenY);
              } else {
                ctx.lineTo(screenX, screenY);
              }
              
              if (i === spokes - 1) {
                ctx.closePath();
                ctx.stroke();
              }
            }
          }

          for (let z = 1.5; z < ringsTwo; z++) {
            const scale = fov / (fov + z * depthSpacing);
            const radius = baseRadius * scale;
            
            // Calculate an angular offset for each ring
            const rotationOffset = z * 0.125; // Gradual angular shift for each deeper ring
            
            // Draw each ring's spokes
            for (let i = 0; i < spokesTwo; i++) {
              const angle = (i / spokesTwo) * Math.PI * .05 + rotationOffset + time * 0.01;
              
              const x = Math.cos(angle) * radius;
              const y = Math.sin(angle) * radius;
              
              const screenX = centerX() + x;
              const screenY = centerY() + y + yOffset;
              
              if (i === 0) {
                ctx.beginPath();
                ctx.moveTo(screenX, screenY);
              } else {
                ctx.lineTo(screenX, screenY);
              }
              
              if (i === spokesTwo - 1) {
                ctx.closePath();
                ctx.stroke();
              }
            }
          }
          
          // Draw the spokes for each ring
          for (let i = 0; i < spokes; i++) {
            const angle = (i / spokes) *  time * 2; // Main angle for spokes
            ctx.beginPath();
            
            for (let z = 1; z < rings; z++) {
              const scale = fov / (fov + z * depthSpacing);
              const radius = baseRadius * scale;
              
              const x = Math.cos(angle) * radius;
              const y = Math.sin(angle) * radius;
              
              const screenX = centerX() + x;
              const screenY = centerY() + y + yOffset;
              
              if (z === 1) {
                ctx.moveTo(screenX, screenY);
              } else {
                ctx.lineTo(screenX, screenY);
              }
            }
            
            ctx.stroke();
          }
          // Draw the spokes for each ring
          for (let i = 0; i < spokesTwo; i++) {
            const angle = (i / spokesTwo) * Math.PI * 2 + time * 0; // Main angle for spokes
            ctx.beginPath();
            
            for (let z = 1; z < ringsTwo; z++) {
              const scale = fov / (fov + z * depthSpacing);
              const radius = baseRadius * scale;
              
              const x = Math.cos(angle) * radius;
              const y = Math.sin(angle) * radius;
              
              const screenX = centerX() + x;
              const screenY = centerY() + y + yOffset;
              
              if (z === 1) {
                ctx.moveTo(screenX, screenY);
              } else {
                ctx.lineTo(screenX, screenY);
              }
            }
            
            ctx.stroke();
          }
    }

    
    
    
    
    function drawPlayer(yOffset = -18) {  //Bottom Triangle
      ctx.fillStyle = '#8efaf2';
      ctx.beginPath();
      ctx.moveTo(centerX(), centerY() - - 8);
      ctx.lineTo(centerX() - 8, centerY() + yOffset + 8);
      ctx.lineTo(centerX() + 8, centerY() + yOffset + 8);
      ctx.closePath();
      ctx.fill();
    }
    function drawPlayerTwo(offsetY = + 35) {  //Top Triangle
        ctx.fillStyle = '#8efaf2';
        ctx.beginPath();
        ctx.moveTo(centerX(), centerY() - 8 - offsetY);
        ctx.lineTo(centerX() + 8, centerY() + 8 - offsetY);
        ctx.lineTo(centerX() - 8, centerY() + 8 - offsetY);
        ctx.closePath();
        ctx.fill();
      }
      function drawPlayerThree(offsetYY = + 18, offsetXX = + 18) {  //Right Triangle
        const x = centerX() + offsetXX;
        const y = centerY() - offsetYY;
        const angle = Math.PI / 1.95; // 90 degrees in radians
        ctx.save();
        ctx.translate(x, y);    // Move origin to triangle center
        ctx.rotate(angle);      // Rotate 90 degrees clockwise
        ctx.fillStyle = '#8efaf2';
        ctx.beginPath();
        ctx.moveTo(0, -8);      // Tip (was up, now right)
        ctx.lineTo(8, 8);       // Bottom right
        ctx.lineTo(-8, 8);      // Bottom left
        ctx.closePath();
        ctx.fill();
        ctx.restore();
      }
      function drawPlayerFour(offsetYYY = - 18, offsetXXX = + 18) { //Left Triangle
        const x = centerX() - offsetXXX;
        const y = centerY() + offsetYYY;
        const angle = Math.PI / -1.95; 
        ctx.save();
        ctx.translate(x, y);    
        ctx.rotate(angle);      
        ctx.fillStyle = '#8efaf2';
        ctx.beginPath();
        ctx.moveTo(0, -8);      
        ctx.lineTo(8, 8);       
        ctx.lineTo(-8, 8);      
        ctx.closePath();
        ctx.fill();
        ctx.restore();
      }

    
    
    
    
    /*function drawEnemies() {
        const fov = 100;
        for (let i = 0; i < 10; i++) {
          const z = (i * 50 + time) % 600;
          const scale = fov / (fov + z);
          const angle = (i * 2.5 + time * 0.05)  / spokes * Math.PI * 2;
      
          const x = Math.cos(angle) * 100 * scale;
          const y = Math.sin(angle) * 100 * scale;
      
          ctx.fillStyle = 'hotpink';
          ctx.beginPath();
          ctx.arc(centerX() + x, centerY() + y, 10 * scale, 0, Math.PI * 2);
          ctx.fill();
        }
    }*/
        function drawEnemies() {
            const fov = 300;
            const numEnemies = 60;
            const radius = 200;
          
            for (let i = 0; i < numEnemies; i++) {
              // Use a consistent seed so each enemy has a stable direction
              const angle = (i / numEnemies) * Math.PI * 2;
              const z = 600 - (time + i * 20) % 600;
          
              const scale = fov / (fov + z);
              const x = Math.cos(angle) * radius * scale;
              const y = Math.sin(angle) * radius * scale;
          
              ctx.fillStyle = 'cyan';
              ctx.beginPath();
              ctx.arc(centerX() + x, centerY() + y, 6 * scale, 0, Math.PI * .5);
              ctx.fill();
            }
          }

    
    
    
    
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      drawWeb();
      drawPlayer();
      drawPlayerTwo();
      drawPlayerThree();
      drawPlayerFour();
      drawEnemies();
      time += 3;
      animationId = requestAnimationFrame(animate);
    }

    animate();

    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('resize', resize);
    };
  }, []);

  return (
    <div className='canvasWrapper'>
      <canvas ref={canvasRef} className='splash' />
      <div className='circleBackground'></div>
      <button
        onClick={onFinish}
        className='splashBtn'
      >
        Enter Editor
      </button>
    </div>
  );
}
