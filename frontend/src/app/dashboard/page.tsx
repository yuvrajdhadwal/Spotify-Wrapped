"use client";
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Button from '../Components/Button';
import Heading1 from '../Components/Heading1'
import Radio from "../Components/Radio";
import BodyText from "@/app/Components/BodyText";
import { getCookie } from "@/utils";
import { logError } from '../utils/logger';
import { logInfo } from '../utils/logger';


/*type DashProps = {
    username: string;
}*/
//unused for now but will use later

export default function Dashboard() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(true);

  //check that user is logged in
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
        logError('Error:', error);
        router.push('/');
      });
  }, [router]);

  if (!isAuthenticated) {
    return null; // or a loading spinner
  }

  const handleLogoutClick = async () => {
    const csrfToken = getCookie('csrftoken');

    try {
      const response = await fetch('http://localhost:8000/spotify/logout/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrfToken || '',
        },
        credentials: 'include',
      });

      if (response.ok) {
        router.push('/');
        const data = await response.json();
        logInfo('Login Successful:', data);
      } else if (response.status === 400) {
        logInfo('Response:', response);
      } else {
        logInfo('Response:', response);
      }
    } catch (error) {
        logError('Error:', error);
    }
  };

   return (
       <div className="flex flex-col items-center p-6 space-y-6 min-h-screen">
           <div className="flex-grow flex items-center">
               <Heading1 text="Username again? Yikes"/>
           </div>
           <div className="flex-grow flex items-center">
               <button
                   className="lowercase text-2xl px-6 py-3 border-2 border-amber-950 rounded-2xl bg-gradient-to-tr from-pink-500 to-yellow-500 text-white shadow-lg"
                   onClick={handleLogoutClick}
               >
                   Sign out
               </button>
           </div>
           <div id="radio-group" className="flex-grow flex items-center space-x-4">
               <BodyText text="Choose a time range:"/>
               <Radio name="time_range" value="short_term" text="Past Month"/>
               <Radio name="time_range" value="medium_term" text="Past 6 Months"/>
               <Radio name="time_range" value="long_term" text="Past Year"/>
           </div>
           <div className="flex-grow flex items-center">
               <Button text="Roast Me" url="/wrapped/title"/>
           </div>
           <div id="duo-input" className="flex-grow flex items-center space-x-4">
               <input type="text" placeholder="Friend's Username" className="lowercase p-2 border rounded"/>
               <Button text="Roast Us" url="/wrapped/title"/>
           </div>
           <div id="nav-buttons" className="flex-grow flex items-center space-x-4 mt-auto">
               <Button text="Past Roasts" url="/history/"/>
               <Button text="Duo Requests" url="/requests/"/>
           </div>
       </div>
   );
}
