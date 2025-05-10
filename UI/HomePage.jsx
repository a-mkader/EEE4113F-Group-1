import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';

export default function HomePage() {
  const navigate = useNavigate();
  const [logs, setLogs] = useState([]);
  const [weather, setWeather] = useState(null);

  // 🐧 Fetch deterrent logs from Raspberry Pi
  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const res = await fetch('http://raspberrypi.local:5000/logs'); // Replace with actual endpoint
        const data = await res.json();
        setLogs(data.logs);
      } catch (err) {
        console.error('Failed to fetch logs:', err);
      }
    };

    fetchLogs();
    const interval = setInterval(fetchLogs, 5000);
    return () => clearInterval(interval);
  }, []);

  // ☁️ Fetch Cape Town weather using Open-Meteo (no API key needed)
  useEffect(() => {
    const fetchWeather = async () => {
      try {
        const res = await fetch(
          'https://api.open-meteo.com/v1/forecast?latitude=-33.92&longitude=18.42&current_weather=true'
        );
        const data = await res.json();
        setWeather({
          temp: data.current_weather.temperature,
          wind: data.current_weather.windspeed,
        });
      } catch (err) {
        console.error("Weather fetch failed:", err);
      }
    };

    fetchWeather();
  }, []);

  return (
    <div
      style={{
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        textAlign: 'center',
        backgroundColor: 'transparent',
        color: 'white',
        padding: '20px',
      }}
    >
      <h1 style={{ fontSize: '3rem', marginBottom: '30px' }}>Welcome to Penguin Watch</h1>

      <button onClick={() => navigate('/calibrate')}>Calibrate</button>
      <button onClick={() => navigate('/livestream')}>Livestream</button>
      <button onClick={() => navigate('/deterrents')}>Previous Deterrents</button>

      {/* 📝 Live Logs Section */}
      <div style={{ marginTop: '40px', width: '80%', maxWidth: '500px' }}>
        <h2 style={{ fontSize: '1.5rem' }}>📝 Recent Logs</h2>
        <div style={{
          maxHeight: '150px',
          overflowY: 'auto',
          backgroundColor: '#00000080',
          padding: '10px',
          borderRadius: '8px',
        }}>
          <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
            {logs.map((entry, idx) => (
              <li key={idx} style={{ textAlign: 'left', marginBottom: '5px' }}>{entry}</li>
            ))}
          </ul>
        </div>
      </div>

      {/* ☀️ Cape Town Weather Section */}
      {weather && (
        <div style={{
          marginTop: '40px',
          backgroundColor: '#ffffffcc',
          padding: '15px 25px',
          borderRadius: '10px',
          color: '#000',
          boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
          textAlign: 'center'
        }}>
          <h2 style={{ margin: '0 0 10px' }}>🌤 Cape Town Weather</h2>
          <p style={{ fontSize: '1.2rem', margin: '5px 0' }}>
            Temperature: {weather.temp}°C<br />
            Wind Speed: {weather.wind} km/h
          </p>
        </div>
      )}
    </div>
  );
}
