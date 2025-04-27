import React from 'react';
import './Character.css'; // Import the CSS file

const Character = ({ hat, glasses, shirt, person }) => {
  return (
    <div className="canvas">
      {/* Render the items based on the passed props */}
      {hat && <img src={hat} alt="hat" className="hat" />}
      {glasses && <img src={glasses} alt="glasses" className="glasses" />}
      {shirt && <img src={shirt} alt="shirt" className="shirt" />}
      {person && <img src={person} alt="person" className="person" />}
    </div>
  );
};

export default Character;
