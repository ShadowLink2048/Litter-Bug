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
    alert("About message here")
  };

  return (
    <div className="home-container">
      {/* Leaderboard */}
      <button className="leaderboard-button" onClick={() => setCurrentPage('leaderboard')}>
        🏆
      </button>

      {/* Friends 
      <button className="friends-button" onClick={() => setCurrentPage('friends')}>
        🤝
      </button>
      */}
      

      {/* Counters */}
      <div className="coins-counter">
          <span> ✨ Trash-Coins: {coins}</span>
        </div>


      {/* Character Section */}
      <div className="character-section">
        <img 
          src="placeholder_idle.gif" 
          alt="Character" 
          className="character-image"
          onClick={handleCharacterClick}
        />
        <button className="customize-button" onClick={() => setCurrentPage('customize')}>
          Customize
        </button>
        <button className="letsgo-button" onClick={() => setCurrentPage('walk')}>
          Let's Go!
        </button>
      </div>

      

      
      <button className="about-button" onClick={() => handleAboutClick()}>
        ❓
      </button>
      


    </div>
  );
}

export default HomePage;
