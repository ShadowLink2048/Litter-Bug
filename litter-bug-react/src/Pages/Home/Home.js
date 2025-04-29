// src/pages/Home.js
import { usePage } from '../../PageContext';
import { useState } from 'react';
import './Home.css';

function HomePage() {
  const { setCurrentPage } = usePage();
  const [steps, setSteps] = useState(0); // Example step counter
  const [coins, setCoins] = useState(0);


  const getPointsFromLocalStorage = () => {
    // Get the points from local storage
    const points = localStorage.getItem('userPoints');

    // If points exist, return them, else return a default value (0)
    return points ? parseInt(points, 10) : 0;
  };

  const handleCharacterClick = () => {
    alert("👾 Your Friend Code: 123-456-789");
  };

  const handleAboutClick = () => {
    alert(`🐞 Welcome to Litter-Bug!

Clean up your neighborhood — one piece of trash at a time.
Track down litter, find the right bins, and help keep your world looking awesome!

🎉 Earn coins, customize your look, and level up as you go.

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
          <span>  🍌Fuel: {getPointsFromLocalStorage()}</span>
        </div>


      {/* Character Section */}
      <div className="character-section">
      <img 
        src={getPointsFromLocalStorage() >= 20 ? "ship_fixed.png" : "ship_broken.gif"} 
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
