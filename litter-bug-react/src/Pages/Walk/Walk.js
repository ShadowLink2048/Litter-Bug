// src/pages/Walk.js
import { usePage } from '../../PageContext';
import './Walk.css';

function WalkPage() {
  const { setCurrentPage } = usePage();

  return (
    <div>
      <h1>ℹ️ Walk Page</h1>
      <button onClick={() => setCurrentPage('home')}>Home</button>

    </div>
  );
}

export default WalkPage;
