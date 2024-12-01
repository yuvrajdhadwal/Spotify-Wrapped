import React from "react";
import Image from "next/image";

type ArtistProps = {
    name: string;
    img: string;
    desc: string;
    rank: number;
}

/**
 * Returns a React element containing a div which contains an artist's name, rank, image, and LLM roast
 *
 * @param props.name the artist's name
 * @param props.img the url to the artist image
 * @param props.desc the LLM-generated roast of the artist
 * @param props.rank the artist's rank
 */
function Artist(props: ArtistProps) {
    const altText = props.name + "'s profile picture";
    return (
        <div className={"flex flex-col m-6 overflow-hidden w-2/5"}>
            <div className={"flex flex-row items-center pb-5"}>
                <Image
                    src={props.img}
                    alt={altText}
                    width={160}
                    height={160}
                    className={"mr-10 border-4 border-black object-contain"}
                />
                <h2 className={"text-7xl text-black lowercase text-nowrap"}>#{props.rank} {props.name}</h2>
            </div>
            <p className={"items-start"}>{props.desc}</p>
        </div>
    );
}

export default Artist;