import { useNavigate } from 'react-router-dom';

export default function HomePage() {
  const navigate = useNavigate();
  return (
    <div style={{ background: 'lightblue', height: '100vh', padding: '20px' }}>
      <h2>Home Page</h2>
      <button style={{ backgroundColor: 'blue', color: 'white', margin: '10px' }} onClick={() => navigate('/calibrate')}>Calibrate</button>
      <button style={{ backgroundColor: 'blue', color: 'white', margin: '10px' }} onClick={() => navigate('/livestream')}>Livestream</button>
      <button style={{ backgroundColor: 'blue', color: 'white', margin: '10px' }} onClick={() => navigate('/deterrents')}>Previous Deterrents</button>
      <button style={{ backgroundColor: 'blue', color: 'white', margin: '10px' }} onClick={() => navigate('/warning')}>Warnings</button>
    </div>
  );
}
