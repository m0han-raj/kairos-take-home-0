import React, { useState, useRef, useEffect } from 'react';
import './App.css';

const PaperSummary = ({ paper }) => (
  <div className="paper-summary">
    <h3 className="paper-title">{paper.title}</h3>
    {paper.pdf_link && (
      <a href={paper.pdf_link} target="_blank" rel="noopener noreferrer" className="pdf-link">
        Read Full Paper (PDF)
      </a>
    )}
    <p className="summary-text">{paper.summary}</p>
  </div>
);

export default function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hi! I am the Scientific-Paper Scout. How can I help you with your research today?' },
  ]);
  const [query, setQuery] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userMessage = { sender: 'user', text: query };
    setMessages((prev) => [...prev, userMessage]);
    setQuery('');
    setIsTyping(true);

    try {
      const response = await fetch('http://localhost:5000/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: 'Network response was not ok.' }));
        throw new Error(errorData.error || 'Failed to fetch papers.');
      }

      const data = await response.json();
      let botMessage;

      if (data.papers && data.papers.length > 0) {
        botMessage = { sender: 'bot', papers: data.papers };
      } else if (data.error) {
        botMessage = { sender: 'bot', text: `An error occurred: ${data.error}` };
      } else {
        botMessage = { sender: 'bot', text: "I couldn't find any results for that query." };
      }
      
      setMessages((prev) => [...prev, botMessage]);

    } catch (err) {
      const errorMessage = { sender: 'bot', text: `Error: ${err.message}` };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="app-container">
      <header className="chat-header">
        <h1>Scientific-Paper Scout</h1>
      </header>
      <main className="chat-body">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message-wrapper ${msg.sender}`}>
            <div className="message-content">
              {msg.text}
              {msg.papers && msg.papers.map((paper, pIdx) => <PaperSummary key={pIdx} paper={paper} />)}
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="message-wrapper bot">
            <div className="message-content typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </main>
      <footer className="chat-input-area">
        <form onSubmit={handleSend} className="chat-form">
          <textarea
            ref={inputRef}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend(e)}
            placeholder="e.g., 'Quantum computing breakthroughs in 2023'"
            disabled={isTyping}
            rows={1}
            className="input-textarea"
          />
          <button type="submit" disabled={!query.trim() || isTyping} className="send-button">
            &#9658;
          </button>
        </form>
      </footer>
    </div>
  );
}