// src/pages/AboutPage.js
import { usePage } from '../../PageContext';

function SettingsPage() {
  const { setCurrentPage } = usePage();

  return (
    <div>
      <h1>ℹ️ Settings Page</h1>
      <button onClick={() => setCurrentPage('home')}>Home</button>

    </div>
  );
}

export default SettingsPage;