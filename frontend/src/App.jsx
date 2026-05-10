import { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState({ msg: '', type: '' });
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files[0]) setFile(e.target.files[0]);
  };

  const onUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    setStatus({ msg: 'Analyzing context...', type: 'info' });
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/upload', { method: 'POST', body: formData });
      const data = await res.json();
      if (res.ok) setStatus({ msg: `Ready: ${data.chunks_processed} chunks`, type: 'success' });
    } catch (err) {
      console.error("Critical Upload Error:", err);
      setStatus({ msg: 'Upload Failed', type: 'error' });
    }
  };

  const onChat = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    const userMsg = { role: 'user', text: query };
    setMessages(prev => [...prev, userMsg]);
    setQuery('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMsg.text }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'ai', text: data.answer, sources: data.sources }]);
    } catch (err) {
      console.error("Critical Chat Error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="sidebar-top">
          <div className="logo-container">
            <div className="logo-icon"></div>
            <div className="sidebar-brand">
              <h1>Enterprise AI</h1>
            </div>
          </div>
          <p style={{color: '#64748b', fontSize: '0.85rem', lineHeight: '1.5'}}>
            Advanced RAG architecture for technical document retrieval.
          </p>
          
          <div className="sidebar-image-container">
            <img src="https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=400" alt="AI abstract" />
          </div>

          <div className="upload-card">
            <label htmlFor="file-input" style={{cursor: 'pointer'}}>
              <div style={{fontSize: '1.5rem', marginBottom: '8px'}}>📤</div>
              <p style={{fontWeight: 700, fontSize: '0.9rem'}}>Knowledge Ingestion</p>
              {file && <p style={{color: '#2563eb', fontSize: '0.75rem', marginTop: '5px', fontWeight: 600}}>File: {file.name}</p>}
            </label>
            <input id="file-input" type="file" accept=".pdf" style={{display: 'none'}} onChange={handleFileChange} />
          </div>
          <button className="btn-primary" onClick={onUpload} disabled={!file}>INGEST KNOWLEDGE</button>
          
          {status.msg && (
            <p style={{
              textAlign: 'center', 
              fontSize: '0.8rem', 
              marginTop: '12px', 
              fontWeight: 600,
              color: status.type === 'success' ? '#10b981' : '#3b82f6'
            }}>
              {status.msg}
            </p>
          )}
        </div>
        <footer style={{fontSize: '0.7rem', color: '#94a3b8', textAlign: 'center'}}>@Copyright Unp12 • SECURE_ENV • V1.3</footer>
      </aside>

      {/* CHAT MAIN */}
      <main className="chat-section">
        <header className="chat-header">
          <div style={{display: 'flex', alignItems: 'center', gap: '10px'}}>
            <span style={{fontSize: '1.2rem'}}>🤖</span>
            <h2 style={{fontSize: '1.1rem', fontWeight: 800}}>Contextual Assistant</h2>
          </div>
          <div style={{color: '#10b981', fontSize: '0.7rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '6px'}}>
            <span style={{width: '8px', height: '8px', background: '#10b981', borderRadius: '50%', boxShadow: '0 0 10px #10b981'}}></span> CORE ONLINE
          </div>
        </header>

        <div className="chat-body">
          {messages.length === 0 && (
            <div style={{margin: 'auto', textAlign: 'center'}}>
              <div style={{fontSize: '3.5rem', marginBottom: '15px'}}>✨</div>
              <h3 style={{color: '#0f172a', fontSize: '1.5rem', fontWeight: 700}}>Ready for Analysis</h3>
              <p style={{color: '#94a3b8', fontSize: '0.95rem', marginTop: '8px'}}>Upload a PDF document to begin context-aware querying.</p>
            </div>
          )}
          {messages.map((m, i) => (
            <div key={i} className="message-row">
              <div className={`message ${m.role}`}>{m.text}</div>
              {m.sources && <div style={{fontSize: '0.7rem', marginTop: '5px', color: '#64748b', textAlign: m.role === 'user' ? 'right' : 'left', fontWeight: 600}}>Sources: {m.sources.join(', ')}</div>}
            </div>
          ))}
          {loading && <div style={{paddingLeft: '40px', color: '#64748b', fontStyle: 'italic', fontSize: '0.9rem'}}>Reasoning...</div>}
        </div>

        <footer className="input-footer">
          <form className="input-wrapper" onSubmit={onChat}>
            <input 
              type="text"
              value={query} 
              onChange={e => setQuery(e.target.value)} 
              placeholder="Ask anything about your documents..." 
              disabled={loading}
            />
            <button type="submit" className="send-btn" disabled={loading || !query.trim()}>
              {loading ? '...' : 'QUERY'}
            </button>
          </form>
        </footer>
      </main>
    </div>
  );
}

export default App;