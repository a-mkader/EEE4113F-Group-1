import { useNavigate } from 'react-router-dom';

export default function HelloPage() {
  const navigate = useNavigate();
  return (
    <div style={{ background: 'white', height: '100vh', textAlign: 'center', paddingTop: '20%' }}>
      <h1 style={{ fontSize: '4rem' }}>🐧</h1>
      <button onClick={() => navigate('/home')}>Start</button>
    </div>
  );
}

