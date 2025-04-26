// src/pages/Leaderboard.js
import { usePage } from '../../PageContext';
import './Leaderboard.css';

function LeaderboardPage() {
    const { setCurrentPage } = usePage();
  
    return (
      <div>
        <h1>Leaderboard Page</h1>
        <button onClick={() => setCurrentPage('home')}>Back to Home</button>
      </div>
    );
  }
  
  export default LeaderboardPage;
