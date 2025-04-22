import { useState, useEffect } from "react";

export default function useLoadingDots(loading) {
  const [loadingDots, setLoadingDots] = useState("");

  useEffect(() => {
    if (!loading) {
      setLoadingDots(""); // Reset when not loading
      return;
    }

    const interval = setInterval(() => {
      setLoadingDots(prev => (prev.length >= 5 ? "" : prev + "."));
    }, 500);

    return () => clearInterval(interval);
  }, [loading]);

  return loadingDots;
}
