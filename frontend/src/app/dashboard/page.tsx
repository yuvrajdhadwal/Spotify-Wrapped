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
    fetch('http://localhost:8000/spotify/is-authenticated/', { credentials: 'include' })
        .then(response => response.json())
      .then(data => {
        if (!data.status) {
            setIsAuthenticated(false);
          router.push('/');
        } else {
            setIsAuthenticated(true);
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
        <Heading1 text = "Username again? Yikes"/>
        <div id="radio-group" className="flex flex-col">
            choose a time range:
            <Radio name = "time_range" value = "short_term>" text = "Past Month"/>
            <Radio name = "time_range" value = "medium_term>" text = "Past 6 Months"/>
            <Radio name = "time_range" value = "long_term>" text = "Past Year"/>
        </div>
        <Button text = "Roast Me" url = "/wrapped/title"/>
        <div id = "duo-input">
            <input type = "text" placeholder = "Friend's Username" className="lowercase"/>
            <Button text = "Roast Us" url = "/wrapped/title"/>
        </div>

        <div id = "nav-buttons">
            <Button text = "Past Roasts" url = "/history/"/>
            <Button text = "Duo Requests" url = "/requests/"/>
        </div>
    </>
  );
}
