import { useEffect, useState } from 'react';
import "../../public/fonts/nintendo-nes-font.ttf"


const TypewriterText = ({ text, speed = 50, onComplete }) => {
  const [displayedText, setDisplayedText] = useState('');
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (index < text.length) {
      const timeout = setTimeout(() => {
        setDisplayedText((prev) => prev + text[index]);
        setIndex(index + 1);
      }, speed);
      return () => clearTimeout(timeout);
    } else if (onComplete) {
      onComplete();
    }
  }, [index, text, speed, onComplete]);

  return (
    <p className="typewriterTxt" style={{ fontFamily: 'NintendoNES' }}>
      {displayedText}
      <span className="blinking-cursor">▮</span>
    </p>
  );
};

export default TypewriterText;
