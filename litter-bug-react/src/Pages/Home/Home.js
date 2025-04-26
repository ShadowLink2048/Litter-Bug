// src/pages/HomePage.js
import { usePage } from '../../PageContext';

function HomePage() {
  const { setCurrentPage } = usePage();

  return (
    <div>
      <h1>🏠 Home Page</h1>
      <button onClick={() => setCurrentPage('about')}>Go to About</button>
    </div>
  );
}

export default HomePage;
