// src/pages/Home.js
import { usePage } from '../../PageContext';
import { useState } from 'react';
import './Home.css';

function HomePage() {
  const { setCurrentPage } = usePage();
  const [steps, setSteps] = useState(0); // Example step counter
  const [coins, setCoins] = useState(0);



  const handleCharacterClick = () => {
    alert("👾 Your Friend Code: 123-456-789");
  };

  const handleAboutClick = () => {
    alert(`🐞 Help!

Litter-bug's ship crash landed in YOUR neighborhood. 
Track down litter to help him fuel his ship, and heal the earth along the way.

🌎 It’s your planet. Let’s clean it up — and have some fun while we’re at it!`)
  };

  return (
    <div className="home-container">
      {/* Leaderboard */}
      

      {/* Friends 
      <button className="friends-button" onClick={() => setCurrentPage('friends')}>
        🤝
      </button>
      */}
      

      {/* Counters */}
      <div className="coins-counter">
          <span>  🍌Fuel: {coins}</span>
        </div>


      {/* Character Section */}
      <div className="character-section">
        <img 
          src="ship_broken.gif" 
          alt="Character" 
          className="character-image"
          onClick={handleCharacterClick}
        />

        <button className="letsgo-button" onClick={() => setCurrentPage('walk')}>
          Let's Go!
        </button>
      </div>

      
      <button className="leaderboard-button" onClick={() => setCurrentPage('leaderboard')}>
        🏆
      </button>
      
      <button className="about-button" onClick={() => handleAboutClick()}>
        ❓
      </button>
      


    </div>
  );
}

export default HomePage;
