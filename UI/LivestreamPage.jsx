// File: src/pages/LivestreamPage.jsx
import { useNavigate } from 'react-router-dom';

export default function LivestreamPage() {
  const navigate = useNavigate();
  return (
    <div style={{ backgroundColor: 'blue', height: '100vh', padding: '20px' }}>
      <h2 style={{ color: 'white' }}>Live Stream</h2>
      <iframe src="http://raspberrypi.local:8000" width="100%" height="80%" title="Livestream"></iframe>
      <button onClick={() => navigate('/home')}>Return to Home</button>
    </div>
  );
}