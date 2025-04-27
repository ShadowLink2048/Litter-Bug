// src/pages/Login.js
import { useState } from 'react';
import { usePage } from '../../PageContext';
import './Login.css';

function LoginPage() {
  const { setCurrentPage } = usePage();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = () => {
    const savedUser = JSON.parse(localStorage.getItem('user'));
  
    if (savedUser && username === savedUser.username && password === savedUser.password) {
      setError('');
      setCurrentPage('home');
    } else {
      setError('Invalid username or password.');
    }
  };
  

  return (
    <div className="login-page">
      <div className="logo">Litter-Bug.ai</div>
      
      <div className="login-box">
        <img src="animation.gif" alt="Login gif" style={{ width: '200px', height: '150px' }} />        
        <h2>Log In</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && <div className="error">{error}</div>}
        <button onClick={handleLogin}>Log In</button>
        <p className="signup-link" onClick={() => setCurrentPage('signup')}>
          Not a member? <span>Sign up!</span>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
