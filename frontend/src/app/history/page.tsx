'use client';
import React, { useEffect, useState } from 'react';
import { useRouter } from "next/navigation";
import Heading1 from '../Components/Heading1';
import BodyText from "@/app/Components/BodyText";

export default function History() {
    const [history, setHistory] = useState<number[]>([]);
    const router = useRouter();

    async function fetchSummary(): Promise<void> {
        try {
            const response = await fetch(`http://localhost:8000/spotify_data/displayhistory`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            });

            if (!response.ok) {
                console.error("Failed to fetch SpotifyUser data");
                return;
            }
            const data = await response.json();
            console.log('Data fetched successfully:', data);
            setHistory(data); // Update state with the fetched data
        } catch (error) {
            console.error("Error fetching SpotifyUser data:", error);
        }
    }

    useEffect(() => {
        fetchSummary().catch(console.error);
    }, []);

    const handleButtonClick = (value: number) => {
        // Store the clicked value in localStorage
        localStorage.setItem('id', value.toString());

        // Redirect to another page
        router.push('/wrapped/title');
    };
    return (
        <>
            <Heading1 text="Past Roasts" />
            <BodyText text="Roast history information" />
            <div className="flex flex-wrap gap-2 mt-4">
                {history.map((item, index) => (
                    <button
                        key={index}
                        onClick={() => handleButtonClick(item)}
                        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                    >
                        {item}
                    </button>
                ))}
            </div>
        </>
    );
}
