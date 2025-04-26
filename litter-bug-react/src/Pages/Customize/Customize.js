// src/pages/AboutPage.js
import { usePage } from '../../PageContext';

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