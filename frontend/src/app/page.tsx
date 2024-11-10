"use client";
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
  const checkAuthentication = async () => {
    try {
      const response = await fetch('http://localhost:8000/spotify/is-authenticated/', {
        credentials: 'include'
      });
      const data = await response.json();

      if (data.status) {
        router.push('/dashboard');
      } else {
        setIsAuthenticated(false);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  checkAuthentication();
  }, [router]);

  const handleLoginClick = () => {
    window.location.href = 'http://localhost:8000/spotify/get-auth-url/';
  };

  if (isAuthenticated) {
    return null; // or a loading spinner
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-7xl font-bold mb-4 text-black">spotify roaster</h1>
      <h2 className="text-4xl mb-8 text-black">your music taste has never been so embarrassing</h2>
      <button
        className="bg-spUIGreen text-white px-6 py-3 rounded-full hover:bg-spGreen"
        onClick={handleLoginClick}
      >
        Login with Spotify
      </button>
    </div>
  );
}
