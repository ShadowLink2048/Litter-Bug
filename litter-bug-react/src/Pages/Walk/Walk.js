import { usePage } from '../../PageContext';
import { useState } from 'react';
import './Walk.css';

function WalkPage() {


  const getPointsFromLocalStorage = () => {
    // Get the points from local storage
    const points = localStorage.getItem('userPoints');

    // If points exist, return them, else return a default value (0)
    return points ? parseInt(points, 10) : 0;
  };


  const { setCurrentPage } = usePage();
  const [coins, setCoins] = useState(0); // Trash-Coins state

  const handleAboutClick = () => {
    alert(`🐞 Welcome to Litter-Bug!

Track your progress as you walk and clean up the neighborhood. Take pictures of the trash you pick up and throw away to earn Trash-Coins!

🎉 Keep it up and level up your character by cleaning the streets!`);
  };

  const handleTakePickUpPhoto = () => {
    alert("📸 Make sure to hold your finding close to the photo, with the logo clearly visible.");
    setCurrentPage('garbagephoto');
  };

  const handleTakeThrowAwayPhoto = () => {
    alert("📸 Make sure your photograph shows the garbage item and the garbage can in the same shot.");
    setCoins(coins + 10); // Example increment for taking a photo
    setCurrentPage('throwawayphoto');

  };

  return (
    <div className="walk-container">
      {/* Trash-Coins */}
      <div className="coins-counter">
        <span> ✨ Trash-Coins: {getPointsFromLocalStorage()}</span>
      </div>

      {/* Leave button */}
      <button className="leave-button" onClick={() => setCurrentPage('home')}>
      👉
      </button>

      {/* Character Image */}
      <div className="character-section">
        <div className="character-wrapper">
          <img 
            src="earth.png" 
            alt="Planet" 
            className="planet-image"
          />
          <img 
            src="white_walk.gif" 
            alt="Character" 
            className="character-image"
          />
        </div>
      </div>


      

      {/* Action Buttons */}
      <div className="action-buttons">
        <button className="action-button" onClick={handleTakePickUpPhoto}>
        🥤🍌 Pick Up Trash 🍎🥡
        </button>
        <button className="action-button" onClick={handleTakeThrowAwayPhoto}>
        🗑️ Throw Away Trash ♻️
        </button>
      </div>

      {/* About Button */}
      <button className="about-button" onClick={handleAboutClick}>
        ❓
      </button>

      <button className="leaderboard-button" onClick={() => setCurrentPage('leaderboard')}>
        🏆
      </button>
    </div>
  );
}

export default WalkPage;
