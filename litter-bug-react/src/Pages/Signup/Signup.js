// src/pages/Signup.js
import { useState } from 'react';
import { usePage } from '../../PageContext';
import './Signup.css'; // we reuse the same CSS!

function SignupPage() {
  const { setCurrentPage } = usePage();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSignup = () => {
    const savedUser = JSON.parse(localStorage.getItem('user'));

    if (savedUser && savedUser.username === username) {
      setError('Username already exists.');
      return;
    }

    const newUser = { username, password };
    localStorage.setItem('user', JSON.stringify(newUser));
    setError('');
    alert('Signup successful! Please log in.');
    setCurrentPage('login');
  };

  return (
    <div className="login-page">
      <div className="logo">Litter Bug</div>
      
      <div className="login-box">
        <h2>Sign Up</h2>
        <input
          type="text"
          placeholder="Choose a username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Choose a password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && <div className="error">{error}</div>}
        <button onClick={handleSignup}>Sign Up</button>
        <p className="signup-link" onClick={() => setCurrentPage('login')}>
          Already have an account? <span>Log in!</span>
        </p>
      </div>
    </div>
  );
}

export default SignupPage;
