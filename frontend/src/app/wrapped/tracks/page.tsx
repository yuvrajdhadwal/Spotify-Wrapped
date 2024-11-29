'use client';
import React, { useEffect, useState } from 'react';
import Track from "@/app/Components/Track";

document.addEventListener('click', () => {window.location.href = "./quirky/"});

export default function Tracks() {
    const [tracks, setTracks] = useState<any[]>([]);

    const [timeRange, setTimeRange] = useState<number>(() => {
        // Load the initial value from localStorage or default to 2
        return parseInt(localStorage.getItem("timeRange") || "2", 10);
    });

    useEffect(() => {
        const storedTimeRange = localStorage.getItem("timeRange");
        if (storedTimeRange) {
            setTimeRange(parseInt(storedTimeRange, 10));
        }
    }, []);

    async function fetchFavoriteSongs(): Promise<void> {
        try {
            const response = await fetch(`http://localhost:8000/spotify_data/displaytracks?timeframe=${timeRange}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include'
            });

            if (!response.ok) {
                console.error("Failed to fetch SpotifyUser data");
                return;
            }
            let data = await response.json();
            console.log('everything went alright');
            console.log(data);
            
            setTracks(data.slice(0, 5));
        } catch (error) {
            console.error("Error fetching SpotifyUser data:", error);
        }
    }

    useEffect(() => {
        fetchFavoriteSongs().catch(console.error);
    }, []);    
    
    return (
        <div className={"flex flex-row justify-center"}>
            {tracks.length > 0 ? (
                tracks.map((track, index) => (
                    <Track
                        key={index}
                        name={track.name}
                        artist={track.artist}
                        img={track.image} // Ensure `image` is the correct field in your API response
                        desc={track.desc}
                        rank={index + 1}
                    />
                ))
            ) : (
                <p>Loading tracks...</p> // Display a simple loading message while fetching data
            )}
        </div>
    );
}