// src/pages/Customize.js
import { usePage } from '../../PageContext';
import './Customize.css';

function CustomizePage() {
  const { setCurrentPage } = usePage();

  return (
    <div>
      <h1>Customize Page</h1>
      <button onClick={() => setCurrentPage('home')}>Back to Home</button>
    </div>
  );
}

export default CustomizePage;
