'use client';
import React, { useEffect, useState } from 'react';
// import Image from 'next/image';
// import Heading2 from "@/app/Components/Heading2";
import Artist from "@/app/Components/Artist";

export default function Artists() {
    const longDesc = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In ultricies pellentesque lobortis. Etiam luctus neque volutpat enim pulvinar vulputate. Praesent rhoncus faucibus magna a venenatis.";
    const [artists, setArtists] = useState<any[]>([]);

    // FIX ME
    const timeframe = 2;

    async function fetchFavoriteArtists(): Promise<void> {
        try {
            const response = await fetch(`http://localhost:8000/spotify_data/displayartists1?timeframe=${timeframe}`, {
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