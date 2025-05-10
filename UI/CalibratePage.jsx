// File: src/pages/CalibratePage.jsx
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

export default function CalibratePage() {
  const navigate = useNavigate();
  const [status, setStatus] = useState('Idle');

  const handleCalibrate = async () => {
    setStatus('Calibrating...');

    try {
      const res = await fetch('http://raspberrypi.local:5000/calibrate'); // Replace with actual endpoint
      const data = await res.json();

      if (data.status === 'done') {
        setStatus('✅ Calibration complete!');
      } else {
        setStatus('⚠️ Unexpected response');
      }
    } catch (err) {
      console.error(err);
      setStatus('❌ Failed to calibrate');
    }
  };

  return (
    <div
      style={{
        padding: '20px',
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        color: 'white',
        textAlign: 'center',
      }}
    >
      <h2>Calibration Page</h2>
      <button onClick={handleCalibrate}>Start Calibration</button>
      <p style={{ marginTop: '20px', fontSize: '1.2rem' }}>{status}</p>
      <button style={{ marginTop: '30px' }} onClick={() => navigate('/home')}>Return to Home</button>
    </div>
  );
}
