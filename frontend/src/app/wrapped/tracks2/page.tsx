'use client';
import React, { useEffect, useState } from 'react';
import Track from "@/app/Components/Track";
import { useRouter } from "next/navigation";

export default function Tracks2() {
    const [tracks, setTracks] = useState<any[]>([]);
    const router = useRouter();

    // Handle click to navigate to the next page
    useEffect(() => {
        const handleClick = () => {
            router.push('/wrapped/quirky/');
        };
        document.addEventListener('click', handleClick);

        return () => {
            document.removeEventListener('click', handleClick);
        };
    }, [router]);

    // Retrieve remaining tracks from localStorage
    useEffect(() => {
        const tracksList = localStorage.getItem("tracksList");
        if (tracksList) {
            setTracks(JSON.parse(tracksList));
        }
    }, []);

    return (
        <div className={"flex flex-row justify-center"}>
            {tracks.length > 0 ? (
                tracks.map((track, index) => (
                    <Track
                        key={index}
                        name={track.name}
                        artist={track.artist}
                        img={track.image} // Ensure `image` matches your API response
                        desc={track.desc}
                        rank={index + 3}
                    />
                ))
            ) : (
                <p>Loading tracks...</p>
            )}
        </div>
    );
}
