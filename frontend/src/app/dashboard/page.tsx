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
import login from '../login/page';


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
            logInfo('hold on a second', data)
            window.location.href = 'http://localhost:8000/spotify/get-auth-url/';
            setIsAuthenticated(true);
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
       <div className="flex flex-col items-center p-6 space-y-6 min-h-screen justify-center">
           <div>
               <Heading1 text="Username again? Yikes"/>
           </div>
           <div className={"items-center justify-center"}>
               <Button text={"Sign Out"} method={handleLogoutClick}/>
           </div>
           <form className={"flex flex-grow flex-col"}>
               <div id="radio-group" className="flex-row flex items-center space-x-4 mt-10">
                   <BodyText text="Choose a time range:"/>
                   <Radio name="time_range" value="short_term" text="Past Month"/>
                   <Radio name="time_range" value="medium_term" text="Past 6 Months"/>
                   <Radio name="time_range" value="long_term" text="Past Year"/>
               </div>
               <div className={"flex items-center justify-center flex-col"}>
               <input type="text" placeholder="(Optional) Friend's Username" className="lowercase p-2 border rounded mt-4"/>
               <Button text="Generate Roast" url="/wrapped/title" extraClasses={"mt-10"}/>
               </div>
           </form>
           <div id="nav-buttons" className="flex items-center space-x-4">
               <Button text="Past Roasts" url="/history/"/>
               <Button text="Duo Requests" url="/requests/"/>
           </div>
       </div>
   );
}
