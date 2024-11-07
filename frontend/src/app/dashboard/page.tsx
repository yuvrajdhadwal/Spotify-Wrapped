"use client";
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Button from '../Components/Button';
import Heading1 from '../Components/Heading1'
import Radio from "../Components/Radio";

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
    <>
        <Heading1 text = "Username again? Yikes"></Heading1>
        <div id="radio-group" className="flex flex-col">
            choose a time range:
            <Radio name = "time_range" value = "short_term>" text = "Past Month"></Radio>
            <Radio name = "time_range" value = "medium_term>" text = "Past 6 Months"></Radio>
            <Radio name = "time_range" value = "long_term>" text = "Past Year"></Radio>
        </div>
        <Button text = "Roast Me" url = "/"></Button>
        <div id = "duo-input">
            <input type = "text" placeholder = "Friend's Username" className="lowercase"></input>
            <Button text = "Roast Us" url = "/"></Button>
        </div>

        <div id = "nav-buttons">
            <Button text = "Past Roasts" url = "/"></Button>
            <Button text = "Duo Requests" url = "/"></Button>
        </div>
    </>
  );
}
