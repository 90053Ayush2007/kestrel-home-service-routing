import { useState, useEffect } from 'react';
import type { FormEvent } from 'react';
import './index.css';

interface RouteResponse {
  predicted_team: string;
  confidence: number;
  reasons: string[];
  signals: Record<string, any>;
  model_version: string;
  needs_review: boolean;
  review_reason: string | null;
}

interface ModelInfo {
  model_version: string;
  metrics: {
    accuracy: number;
    macro_f1: number;
    train_size: number;
    val_size: number;
  };
}

const sampleRecords = [
  {
    request_id: "REQ-001",
    channel: "email",
    product_family: "Air Purifier",
    warranty_status: "in_warranty",
    request_text: "My purifier is making a loud noise when turned on. It sounds like a motor issue.",
  },
  {
    request_id: "REQ-002",
    channel: "whatsapp",
    product_family: "Water Purifier",
    warranty_status: "out_of_warranty",
    request_text: "I was charged twice for the AMC renewal yesterday. Please refund.",
  },
  {
    request_id: "REQ-003",
    channel: "chat",
    product_family: "Mixer Grinder",
    warranty_status: "in_warranty",
    request_text: "Where is my replacement jar? I asked for a return 5 days ago.",
  }
];

function App() {
  const [formData, setFormData] = useState({
    request_id: "",
    channel: "email",
    product_family: "Air Purifier",
    warranty_status: "in_warranty",
    request_text: "",
  });
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RouteResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/model-info')
      .then(res => res.json())
      .then(data => setModelInfo(data))
      .catch(err => console.error("Could not fetch model info", err));
  }, []);

  const loadSample = (index: number) => {
    setFormData(sampleRecords[index]);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const payload = {
        ...formData,
        source: "crm",
        created_at_ist: new Date().toISOString()
      };
      
      const res = await fetch('http://localhost:8000/api/route', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      if (!res.ok) {
        throw new Error(`Server returned ${res.status}`);
      }
      
      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Failed to connect to API.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>Kestrel Home | Service Routing</h1>
        <p style={{ color: 'var(--text-muted)' }}>AI-powered automatic destination routing for customer service requests</p>
      </header>

      <div className="grid">
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2 style={{ margin: 0 }}>Request Details</h2>
            <div>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginRight: '0.5rem' }}>Load Sample:</span>
              <button className="badge badge-primary" style={{ border: 'none', cursor: 'pointer', marginRight: '4px' }} onClick={() => loadSample(0)}>1</button>
              <button className="badge badge-primary" style={{ border: 'none', cursor: 'pointer', marginRight: '4px' }} onClick={() => loadSample(1)}>2</button>
              <button className="badge badge-primary" style={{ border: 'none', cursor: 'pointer' }} onClick={() => loadSample(2)}>3</button>
            </div>
          </div>
          
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Request ID</label>
              <input type="text" className="form-control" value={formData.request_id} onChange={e => setFormData({...formData, request_id: e.target.value})} required />
            </div>
            
            <div style={{ display: 'flex', gap: '1rem' }}>
              <div className="form-group" style={{ flex: 1 }}>
                <label>Channel</label>
                <select className="form-control" value={formData.channel} onChange={e => setFormData({...formData, channel: e.target.value})}>
                  <option value="email">Email</option>
                  <option value="whatsapp">WhatsApp</option>
                  <option value="chat">Chat</option>
                  <option value="ivr">IVR</option>
                </select>
              </div>
              <div className="form-group" style={{ flex: 1 }}>
                <label>Warranty Status</label>
                <select className="form-control" value={formData.warranty_status} onChange={e => setFormData({...formData, warranty_status: e.target.value})}>
                  <option value="in_warranty">In Warranty</option>
                  <option value="out_of_warranty">Out of Warranty</option>
                  <option value="shield">Kestrel Shield</option>
                </select>
              </div>
            </div>
            
            <div className="form-group">
              <label>Product Family</label>
              <input type="text" className="form-control" value={formData.product_family} onChange={e => setFormData({...formData, product_family: e.target.value})} required />
            </div>
            
            <div className="form-group">
              <label>Customer Message</label>
              <textarea className="form-control" value={formData.request_text} onChange={e => setFormData({...formData, request_text: e.target.value})} required placeholder="Enter the customer issue..." />
            </div>
            
            <button type="submit" className="btn" disabled={loading}>
              {loading ? <span className="spinner"></span> : "Route Request"}
            </button>
          </form>
        </div>

        <div className="card result-section">
          <h2 style={{ margin: '0 0 1rem 0' }}>Routing Decision</h2>
          
          {error && (
            <div className="alert alert-danger">
              <strong>Error:</strong> {error}
            </div>
          )}

          {!result && !error && !loading && (
            <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '2rem 0' }}>
              Submit a request to see the routing decision.
            </div>
          )}

          {result && (
            <>
              {result.needs_review && (
                <div className="alert alert-warning">
                  <strong>⚠️ Human Review Recommended</strong><br/>
                  {result.review_reason}
                </div>
              )}
              
              <div className="stat-box" style={{ borderLeft: `4px solid ${result.needs_review ? 'var(--warning)' : 'var(--success)'}` }}>
                <h3>Predicted Destination Team</h3>
                <p style={{ color: result.needs_review ? 'var(--warning)' : 'var(--success)' }}>
                  {result.predicted_team}
                </p>
              </div>
              
              <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem' }}>
                <div className="stat-box" style={{ flex: 1 }}>
                  <h3>Confidence</h3>
                  <p>{(result.confidence * 100).toFixed(1)}%</p>
                </div>
                <div className="stat-box" style={{ flex: 1 }}>
                  <h3>Model Version</h3>
                  <p style={{ fontSize: '1rem' }}>{result.model_version}</p>
                </div>
              </div>

              <div className="stat-box" style={{ marginTop: '0.5rem' }}>
                <h3>Reasoning</h3>
                <ul style={{ margin: '0.5rem 0 0 0', paddingLeft: '1.2rem', color: 'var(--text-muted)' }}>
                  {result.reasons.map((r, i) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>
              </div>
            </>
          )}

          <div style={{ marginTop: 'auto', paddingTop: '2rem' }}>
            <h3 style={{ margin: '0 0 1rem 0', borderBottom: '1px solid var(--border)', paddingBottom: '0.5rem' }}>Model Performance (Live Eval)</h3>
            {modelInfo?.metrics ? (
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Validation Accuracy</div>
                  <div style={{ fontWeight: '600' }}>{(modelInfo.metrics.accuracy * 100).toFixed(1)}%</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Macro F1</div>
                  <div style={{ fontWeight: '600' }}>{(modelInfo.metrics.macro_f1 * 100).toFixed(1)}%</div>
                </div>
              </div>
            ) : (
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Loading metrics from backend...</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
