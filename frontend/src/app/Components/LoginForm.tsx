import React, { useState, useEffect, ChangeEvent, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import { logError } from '../utils/logger';
import { logInfo } from '../utils/logger';
import Button from "./Button";

interface FormData {
  username: string;
  password: string;
}

// Helper function to get CSRF token from cookies
const getCookie = (name: string): string | null => {
  const cookieValue = document.cookie
    .split('; ')
    .find((row) => row.startsWith(name + '='))
    ?.split('=')[1];
  return cookieValue ? decodeURIComponent(cookieValue) : null;
};

const LoginForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({username: '', password: ''});
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    fetch('http://localhost:8000/spotify/get-csrf-token/', {
      credentials: 'include',
    })
        .then((response) => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
        })
        .catch((error) => {
          logError('Error fetching CSRF token:', error);
        });
  }, []);

  const handleSignupRedirect = () => {
    router.push('/signup');
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const {name, value} = e.target;
    setFormData({...formData, [name]: value});
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const csrfToken = getCookie('csrftoken');

    try {
      const response = await fetch('http://localhost:8000/spotify/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrfToken || '',
        },
        body: new URLSearchParams({
          username: formData.username,
          password: formData.password,
        }),
        credentials: 'include',
      });

      if (response.ok) {
        const data = await response.json();
        logInfo('Login sucessful:', data);
        setErrorMessage(null);
        router.push('dashboard/');
      } else if (response.status === 400) {
        setErrorMessage('Login failed. Retype username and password.');
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.error || 'An error occurred. Please try again.');
      }
    } catch (error) {
      logError('Unexpected Error:', error);
      setErrorMessage('An unexpected error occurred. Please try again.');
    }
  };


  return (
      <>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username:</label>
          <input type="text" name="username" value={formData.username} onChange={handleChange} className={"border-2"}/>
        </div>
        <div>
          <label>Password:</label>
          <input type="password" name="password" value={formData.password} onChange={handleChange} className={"border-2"}/>
        </div>
        <Button text={"Login"} method={() => null}/>
        {errorMessage && <p style={{color: 'red'}}>{errorMessage}</p>}
      </form>
  <div>
    <Button text={"Don't Have An Account? Sign Up!"} method={handleSignupRedirect}/>
  </div>
  </>

)
  ;
};

export default LoginForm;
