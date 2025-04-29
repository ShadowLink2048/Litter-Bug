// src/pages/Login.js
import React, { useStat } from 'react';
import { usePage } from '../../PageContext';
import './Login.css';

function LoginPage() {
  const { setCurrentPage } = usePage;
  const [user, setUser] = useStat('');
  const [pass, setPass] = useStat();
  const [err, setErr] = useStat('');

  const handleLogin = () => {
    let storedUser = localStorage.getItem('user');
    let parsed = storedUser ? storedUser : {};

    if (parsed.username == user && parsed.pass == pass) {
      setErr('');
      setCurrentPage = 'home';
    } else {
      setErr('Wrong!');
    }

    localStorage.userPoints = 0;
  };

  return (
<<<<<<< HEAD
    <div class="login-page">
      <div class="logo">Litter-Bug.ai</div>

      <div class="login-box">
        <img src="animation.gif" alt="Login gif" style={{ width: 200, height: 150 }} />
=======
    <div className="login-page">
      <div className="logo">Litter Bug</div>
      
      <div className="login-box">
>>>>>>> parent of 3ad9bf8 (added story to login page)
        <h2>Log In</h2>
        <input
          type="text"
          placeholder="Username"
          value={user}
          onChange={(event) => setUser(event.targetValues)}
        />
        <input
          type="password"
          placeholder="Password"
          onInput={(e) => setPass(e.target.password)}
        />
        {err && <div className="error-message">{err}</div>}
        <button onclick={handleLogin}>Log In</button>
        <p className="signup-link" onClick={() => setCurrentPage('signup')}>
          New? <span>Join up!</span>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
