'use client'
import React, { useEffect, useState } from 'react';

document.addEventListener('click', () => {window.location.href = "./title/"});

export default function Quirky() {
    const [desc, setDesc] = useState<any[]>([]);

    const [timeRange, setTimeRange] = useState<number>(() => {
        return parseInt(localStorage.getItem("timeRange") || "2", 10);
    });

    useEffect(() => {
        const storedTimeRange = localStorage.getItem("timeRange");
        if (storedTimeRange) {
            setTimeRange(parseInt(storedTimeRange, 10));
        }
    }, []);

    async function fetchFavoriteGenres(): Promise<void> {
        try {
            const response = await fetch(`http://localhost:8000/spotify_data/displayquirky?timeframe=${timeRange}`, {
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
            
            setDesc(data)
        } catch (error) {
            console.error("Error fetching SpotifyUser data:", error);
        }
    }

    useEffect(() => {
        fetchFavoriteGenres().catch(console.error);
    }, []);   

    return (
        <div className={"flex flex-row justify-center"}>
            <p>{desc}</p>
            <img 
                src="..\..\images\trashcan.png" 
                alt="trash graphic" 
                style={{ maxWidth: "20%", height: "auto", marginTop: "20px" }}
                />
        </div>
    );
}