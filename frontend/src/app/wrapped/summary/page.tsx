'use client';
import React, { useEffect, useState } from 'react';
import { useRouter } from "next/navigation";
import SummaryComponent from "@/app/Components/Summary";

// Define the type for the summary data
type SummaryData = {
    artists: string[];
    tracks: string[];
    quirky: string;
    genres: string[];
};

export default function Summary() {
    const router = useRouter();
    const [desc, setDesc] = useState<SummaryData | null>(null);

    useEffect(() => {
        const handleClick = () => {
            router.push('/wrapped/title/');
        };
        document.addEventListener('click', handleClick);

        return () => {
            document.removeEventListener('click', handleClick);
        };
    }, [router]);

    async function fetchSummary(): Promise<void> {
        try {
            const response = await fetch(`http://localhost:8000/spotify_data/displaysummary`, {
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
            const data = await response.json();
            console.log('Data fetched successfully:', data);
            setDesc(data);
        } catch (error) {
            console.error("Error fetching SpotifyUser data:", error);
        }
    }

    useEffect(() => {
        fetchSummary().catch(console.error);
    }, []);

    return (
        <div className="flex flex-row justify-center">
            {desc ? (
                <SummaryComponent
                    artists={desc.artists}
                    tracks={desc.tracks}
                    quirky={desc.quirky}
                    genres={desc.genres}
                />
            ) : (
                <p>Loading summary...</p>
            )}
        </div>
    );
}
