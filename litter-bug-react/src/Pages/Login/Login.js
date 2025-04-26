// src/pages/AboutPage.js
import { usePage } from '../../PageContext';

function AboutPage() {
  const { setCurrentPage } = usePage();

  return (
    <div>
      <h1>ℹ️ Login Page</h1>
      <button onClick={() => setCurrentPage('signup')}>Not signed up yet? Sign in</button>
      <button onClick={() => setCurrentPage('home')}>Log in</button>

    </div>
  );
}

export default AboutPage;