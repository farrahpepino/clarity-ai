import './App.css'
import { useEffect, useState } from 'react'
import Hero from './hero/Hero'
import Output from './output/Output'


function App() {
  const [simplifiedText, setSimplifiedText] = useState<string | null>(null);

  useEffect(() => {
    const move = (e: MouseEvent) => {
      document.body.style.backgroundPosition =
        `${e.clientX / 100}px ${e.clientY / 100}px`;
    };

    window.addEventListener("mousemove", move);

    return () => window.removeEventListener("mousemove", move);
  }, []);

  return (
    <div>
      {!simplifiedText ? (
        <>
          <Hero onResult={setSimplifiedText} />
        </>
      ) : (
        <Output text={simplifiedText} />
      )}
    </div>
  )
}

export default App