"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Button from '../Components/Button';
import Heading1 from '../Components/Heading1';
import Radio from "../Components/Radio";
import BodyText from "@/app/Components/BodyText";
import { getCookie } from "@/utils";
import { logError, logInfo } from '../utils/logger';

export default function Dashboard() {
    const router = useRouter();
    const [isAuthenticated, setIsAuthenticated] = useState(true);
    const [username, setUsername] = useState<string>('Guest');
    const [timeframe, setTimeframe] = useState<number>(2);
    
    useEffect(() => {
        localStorage.setItem("id", "-1");
    }, []);

    // Fetch username from backend
    useEffect(() => {
        const fetchUsername = async () => {
            try {
                const response = await fetch('http://localhost:8000/spotify/get-username/', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                setUsername(data.username);
            } catch (error) {
                console.error('Error fetching username:', error);
            }
        };

        fetchUsername();
    }, []);

    // Load `timeRange` from localStorage
    useEffect(() => {
        const storedTimeframe = localStorage.getItem("timeRange");
        if (storedTimeframe) {
            setTimeframe(parseInt(storedTimeframe, 10));
        }
    }, []);

    // Check authentication
    useEffect(() => {
        fetch('http://localhost:8000/spotify/is-authenticated/', { credentials: 'include' })
            .then(response => response.json())
            .then(data => {
                if (!data.status) {
                    logInfo('Not authenticated', data);
                    window.location.href = 'http://localhost:8000/spotify/get-auth-url/';
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
        return null; // Render a loading spinner or a fallback UI here
    }

    const handleSelection = (value: number) => {
        setTimeframe(value); // Update state
        localStorage.setItem("timeRange", value.toString()); // Save to localStorage
    };
    
    return (
        <div className="flex flex-col items-center p-6 space-y-6 min-h-screen justify-center">
            <Heading1 text={`${username} again? Yikes`} />
            <Button text={"Sign Out"} method={() => {}} />
            <Button text={"Delete Account"} method={() => {}} />

            <form className={"flex flex-grow flex-col"} action="/wrapped/title/" method="POST">
                <div id="radio-group" className="flex-row flex items-center space-x-4 mt-10">
                    <BodyText text="Choose a time range:" />
                    <Radio
                        name="time_range"
                        value="short_term"
                        text="Past Month"
                        onChange={() => handleSelection(0)}
                        checked={timeframe === 0}
                    />
                    <Radio
                        name="time_range"
                        value="medium_term"
                        text="Past 6 Months"
                        onChange={() => handleSelection(1)}
                        checked={timeframe === 1}
                    />
                    <Radio
                        name="time_range"
                        value="long_term"
                        text="Past Year"
                        onChange={() => handleSelection(2)}
                        checked={timeframe === 2}
                    />
                </div>
                <input
                    name="other_user"
                    type="text"
                    placeholder="(Optional) Friend's Username"
                    className="lowercase p-2 border rounded mt-4"
                />
                <Button text="Generate Roast" method={() => null} extraClasses="mt-10" />
            </form>

            <div id="nav-buttons" className="flex items-center space-x-4">
                <Button text="Past Roasts" url="/history/" />
                <Button text="Duo Requests" url="/requests/" />
            </div>
        </div>
    );
}
