'use client';
import React, { useEffect, useState } from 'react';
import { useRouter } from "next/navigation";
import Artist from "@/app/Components/Artist";

export default function Artists2() {
    const router = useRouter();
    const [artists, setArtists] = useState<any[]>([]);

    useEffect(() => {
        const handleClick = () => {
            router.push('/wrapped/genres/');
        };
        document.addEventListener('click', handleClick);

        return () => {
            document.removeEventListener('click', handleClick);
        };
    }, [router]);

    // Load remaining artists from localStorage
    useEffect(() => {
        const artistsList = localStorage.getItem("artistsList");
        if (artistsList) {
            setArtists(JSON.parse(artistsList));
        }
    }, []);

    return (
        <div className={"flex flex-row justify-center"}>
            {artists.length > 0 ? (
                artists.map((artist: { name: string; image: string; desc: string; }, index: number) => (
                    <Artist
                        key={index}
                        name={artist.name}
                        img={artist.image} // Ensure `image` matches your API response
                        desc={artist.desc}
                        rank={index + 3}
                    />
                ))
            ) : (
                <p>Loading artists...</p>
            )}
        </div>
    );
}
