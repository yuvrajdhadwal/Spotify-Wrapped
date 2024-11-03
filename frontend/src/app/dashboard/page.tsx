"use client";
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Dashboard() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(true);

  useEffect(() => {
    // Check if the user is authenticated
    fetch('http://127.0.0.1:8000/spotify/is-authenticated/', { credentials: 'include' })
      .then(response => response.json())
      .then(data => {
        if (!data.status) {
          router.push('/');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        router.push('/');
      });
  }, [router]);

  if (!isAuthenticated) {
    return null; // or a loading spinner
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold mb-4 text-black">Welcome to Your Dashboard</h1>
      <p className="text-xl mb-8 text-black">You're now logged in with Spotify!</p>
      {/* Add more dashboard content here */}
    </div>
  );
}
