'use client';
import React, { useEffect, useState } from 'react';
import { useRouter } from "next/navigation";
// import Image from 'next/image';
// import Heading2 from "@/app/Components/Heading2";
import Artist from "@/app/Components/Artist";

export default function Artists() {
    const router = useRouter();

    useEffect(() => {
        const handleClick = () => {
          router.push('/wrapped/genres/');
        };
        document.addEventListener('click', handleClick);
    
        return () => {
          document.removeEventListener('click', handleClick);
        };
      }, [router]);

    const [artists, setArtists] = useState<any[]>([]);

    const [timeRange, setTimeRange] = useState<number>(2);

    useEffect(() => {
        const storedTimeRange = localStorage.getItem("timeRange");
        if (storedTimeRange) {
            setTimeRange(parseInt(storedTimeRange, 10));
        }
    }, []);
    

    async function fetchFavoriteArtists(): Promise<void> {
        const datetimeCreated = localStorage.getItem("datetimeCreated");
        try {
            const response = await fetch(`http://localhost:8000/spotify_data/displayartists?datetimecreated=${datetimeCreated}`, {
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