// Summary.tsx
import React from "react";

type SummaryComponentProps = {
    artists: string[];
    tracks: string[];
    quirky: string;
    genres: string[];
};

const SummaryComponent: React.FC<SummaryComponentProps> = ({ artists, tracks, quirky, genres }) => {
    return (
        <div>
            <h2>Top Artists</h2>
            <ul>
                {artists.map((artist, index) => (
                    <li key={index}>{artist}</li>
                ))}
            </ul>
            <h2>Top Tracks</h2>
            <ul>
                {tracks.map((track, index) => (
                    <li key={index}>{track}</li>
                ))}
            </ul>
            <h2>Quirky Favorite</h2>
            <p>{quirky}</p>
            <h2>Genres</h2>
            <ul>
                {genres.map((genre, index) => (
                    <li key={index}>{genre}</li>
                ))}
            </ul>
        </div>
    );
};

export default SummaryComponent;
