import React, { useState } from 'react';
import axios from 'axios';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, Cell } from 'recharts';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import { Upload, AlertTriangle, CheckCircle, Activity } from 'lucide-react';
import 'leaflet/dist/leaflet.css'; // <--- THIS MAKES THE MAP WORK

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);
  const [anomalies, setAnomalies] = useState(0);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first!");
    
    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/analyze", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const results = response.data.results;
      setData(results);
      
      const count = results.filter(r => r.status === "New Organism").length;
      setAnomalies(count);
      
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to connect to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '40px', fontFamily: 'Arial, sans-serif', maxWidth: '1200px', margin: '0 auto' }}>
      
      {/* HEADER */}
      <header style={{ marginBottom: '40px', borderBottom: '1px solid #ddd', paddingBottom: '20px' }}>
        <h1 style={{ color: '#0f172a', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Activity color="#2563eb" /> JalDrishti: Marine Anomaly Detection
        </h1>
        <p style={{ color: '#64748b' }}>
          Upload eDNA sequencing data to detect unknown marine organisms using Unsupervised ML.
        </p>
      </header>

      {/* UPLOAD SECTION */}
      <div style={{ background: '#f8fafc', padding: '30px', borderRadius: '12px', border: '2px dashed #cbd5e1', textAlign: 'center' }}>
        <input type="file" onChange={handleFileChange} accept=".csv" style={{ marginBottom: '10px' }} />
        <br />
        <button 
          onClick={handleUpload} 
          disabled={loading}
          style={{
            marginTop: '15px', padding: '10px 20px', background: loading ? '#94a3b8' : '#2563eb',
            color: 'white', border: 'none', borderRadius: '6px', cursor: loading ? 'not-allowed' : 'pointer',
            fontSize: '16px', display: 'inline-flex', alignItems: 'center', gap: '8px'
          }}
        >
          {loading ? "Processing DNA..." : <><Upload size={18} /> Analyze Sample</>}
        </button>
      </div>

      {/* RESULTS DASHBOARD */}
      {data.length > 0 && (
        <div style={{ marginTop: '40px' }}>
          
          {/* METRICS */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '40px' }}>
            <div style={{ padding: '20px', background: '#ecfdf5', borderRadius: '8px', border: '1px solid #6ee7b7' }}>
              <h3 style={{ margin: 0, color: '#047857', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <CheckCircle /> Processed Samples
              </h3>
              <p style={{ fontSize: '32px', fontWeight: 'bold', margin: '10px 0 0' }}>{data.length}</p>
            </div>
            <div style={{ padding: '20px', background: '#fef2f2', borderRadius: '8px', border: '1px solid #fca5a5' }}>
              <h3 style={{ margin: 0, color: '#b91c1c', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <AlertTriangle /> New Organisms Detected
              </h3>
              <p style={{ fontSize: '32px', fontWeight: 'bold', margin: '10px 0 0' }}>{anomalies}</p>
            </div>
          </div>

          {/* VISUALIZATION GRID - SIDE BY SIDE */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            
            {/* 1. SCATTER PLOT */}
            <div style={{ border: '1px solid #e2e8f0', borderRadius: '8px', padding: '20px' }}>
              <h3>🧬 Genetic Clusters (PCA)</h3>
              <div style={{ height: '350px', width: '100%' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                    <CartesianGrid />
                    <XAxis type="number" dataKey="pca_x" name="PCA X" />
                    <YAxis type="number" dataKey="pca_y" name="PCA Y" />
                    <RechartsTooltip cursor={{ strokeDasharray: '3 3' }} />
                    <Scatter name="Marine Life" data={data} fill="#8884d8">
                      {data.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.status === 'New Organism' ? '#ef4444' : '#3b82f6'} />
                      ))}
                    </Scatter>
                  </ScatterChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* 2. GEOGRAPHIC MAP */}
            <div style={{ border: '1px solid #e2e8f0', borderRadius: '8px', padding: '20px' }}>
              <h3>🌍 Global Anomaly Map</h3>
              <div style={{ height: '350px', width: '100%', overflow: 'hidden', borderRadius: '8px' }}>
                {/* Center set to Pacific Ocean for our dummy data */}
                <MapContainer center={[20, 140]} zoom={2} style={{ height: '100%', width: '100%' }}>
                  <TileLayer
                    url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
                    attribution='&copy; OpenStreetMap contributors'
                  />
                  {data.map((point, idx) => (
                    <CircleMarker 
                      key={idx}
                      center={[point.Latitude, point.Longitude]}
                      radius={5}
                      pathOptions={{ 
                        color: point.status === 'New Organism' ? '#ef4444' : '#3b82f6',
                        fillColor: point.status === 'New Organism' ? '#ef4444' : '#3b82f6',
                        fillOpacity: 0.7 
                      }}
                    >
                      <Popup>
                        <strong>{point.status}</strong><br />
                        Location: {point.Location}
                      </Popup>
                    </CircleMarker>
                  ))}
                </MapContainer>
              </div>
            </div>

          </div>

        </div>
      )}
    </div>
  );
}

export default App;