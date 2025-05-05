// File: src/pages/PreviousDeterrentsPage.jsx
import { useNavigate } from 'react-router-dom';

export default function PreviousDeterrentsPage() {
  const navigate = useNavigate();
  const data = [
    '2025-05-04 14:22',
    '2025-05-04 09:16',
    '2025-05-03 20:41'
  ];
  return (
    <div style={{ padding: '20px' }}>
      <h2>Previous Deterrents</h2>
      <ul>
        {data.map((entry, i) => <li key={i}>{entry}</li>)}
      </ul>
      <button onClick={() => navigate('/home')}>Return to Home</button>
    </div>
  );
}