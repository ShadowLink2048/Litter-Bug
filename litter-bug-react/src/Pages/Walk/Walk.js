import { usePage } from '../../PageContext';
import { useState } from 'react';
import './Walk.css';

function WalkPage() {
  const { setCurrentPage } = usePage();
  const [coins, setCoins] = useState(0); // Trash-Coins state

  const handleAboutClick = () => {
    alert(`🐞 Welcome to Litter-Bug!

Track your progress as you walk and clean up the neighborhood. Take pictures of the trash you pick up and throw away to earn Trash-Coins!

🎉 Keep it up and level up your character by cleaning the streets!`);
  };

  const handleTakePickUpPhoto = () => {
    alert("📸 Picture of picking up garbage taken!");
    setCoins(coins + 10); // Example increment for taking a photo
  };

  const handleTakeThrowAwayPhoto = () => {
    alert("📸 Picture of throwing away garbage taken!");
    setCoins(coins + 10); // Example increment for taking a photo
  };

  return (
    <div className="walk-container">
      {/* Trash-Coins */}
      <div className="coins-counter">
        <span> ✨ Trash-Coins: {coins}</span>
      </div>

      {/* Leave button */}
      <button className="leave-button" onClick={() => setCurrentPage('home')}>
      👉
      </button>

      {/* Character Image */}
      <div className="character-section">
        <img 
          src="green_walk.gif" 
          alt="Character" 
          className="character-image"
        />
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
