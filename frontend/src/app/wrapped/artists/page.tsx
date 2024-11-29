'use client';
import React, { useEffect, useState } from 'react';
// import Image from 'next/image';
// import Heading2 from "@/app/Components/Heading2";
import Artist from "@/app/Components/Artist";

document.addEventListener('click', () => {window.location.href = "./genres/"});

export default function Artists() {
    const [artists, setArtists] = useState<any[]>([]);

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

    async function fetchFavoriteArtists(): Promise<void> {
        try {
            const response = await fetch(`http://localhost:8000/spotify_data/displayartists?timeframe=${timeRange}`, {
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
            
            setArtists(data.slice(0, 5));
        } catch (error) {
            console.error("Error fetching SpotifyUser data:", error);
        }
    }

    useEffect(() => {
        fetchFavoriteArtists().catch(console.error);
    }, []);    
    
    return (
        <div className={"flex flex-row justify-center"}>
            {artists.length > 0 ? (
                artists.map((artist, index) => (
                    <Artist
                        key={index}
                        name={artist.name}
                        img={artist.image} // Ensure `image` is the correct field in your API response
                        desc={artist.desc}
                        rank={index + 1}
                    />
                ))
            ) : (
                <p>Loading artists...</p> // Display a simple loading message while fetching data
            )}
        </div>
    );
}