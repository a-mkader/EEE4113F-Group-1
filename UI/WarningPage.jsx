// File: src/pages/WarningPage.jsx
import { useNavigate } from 'react-router-dom';

export default function WarningPage() {
  const navigate = useNavigate();
  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1 style={{ color: 'red' }} onClick={() => navigate('/livestream')}>WARNING: Badger detected! (Click here)</h1>
    </div>
  );
}
