// src/pages/AboutPage.js
import { usePage } from '../../PageContext';
import './About.css';

function AboutPage() {
  const { setCurrentPage } = usePage();

  return (
    <div>
      <h1>ℹ️ About Page</h1>
      <button onClick={() => setCurrentPage('home')}>Back to Home</button>
    </div>
  );
}

export default AboutPage;
