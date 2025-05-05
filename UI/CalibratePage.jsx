// File: src/pages/CalibratePage.jsx
import { useNavigate } from 'react-router-dom';

export default function CalibratePage() {
  const navigate = useNavigate();
  return (
    <div style={{ padding: '20px' }}>
      <h2>Calibration Page</h2>
      <button onClick={() => navigate('/home')}>Return to Home</button>
    </div>
  );
}
