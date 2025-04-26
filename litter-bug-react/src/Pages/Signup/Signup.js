// src/pages/Signup.js
import { usePage } from '../../PageContext';
import './Signup.css';

function SignupPage() {
  const { setCurrentPage } = usePage();

  return (
    <div>
      <h1>ℹ️ Signup Page</h1>
      <button onClick={() => setCurrentPage('home')}>Home</button>

    </div>
  );
}

export default SignupPage;
