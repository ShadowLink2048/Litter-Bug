// src/App.js
import './App.css';
import { PageProvider, usePage } from './PageContext';
import HomePage from './Pages/Home/Home.js';
import AboutPage from './Pages/About/About.js';
import CustomizePage from './Pages/Customize/Customize.js';
import LeaderboardPage from './Pages/Leaderboard/Leaderboard.js';
import SettingsPage from './Pages/Settings/Settings.js';
import SignupPage from './Pages/Signup/Signup.js';
import LoginPage from './Pages/Login/Login.js';
import WalkPage from './Pages/Walk/Walk.js';
import FriendsPage from './Pages/Friends/Friends.js'



function PageSwitcher() {
  const { currentPage } = usePage();

  switch (currentPage) {
    case 'home':
      return <HomePage />;
    case 'about':
      return <AboutPage />;
    case 'customize':
      return <CustomizePage />;
    case 'leaderboard':
      return <LeaderboardPage />;
    case 'settings':
      return <SettingsPage />;
    case 'login':
      return <LoginPage />;
    case 'signup':
      return <SignupPage />;
    case 'walk':
      return <WalkPage />;
    case 'friends':
      return <FriendsPage />;
    default:
      return <div>404: Page not found</div>;
  }
}

function App() {
  return (
    <div className="App">
      <PageProvider>
        <PageSwitcher />
      </PageProvider>
    </div>
  );
}

export default App;
