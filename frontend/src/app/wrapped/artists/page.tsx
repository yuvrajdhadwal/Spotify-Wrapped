'use client';
import React, {useEffect} from 'react';
import Image from 'next/image';
import Heading2 from "@/app/Components/Heading2";
import Artist from "@/app/Components/Artist";

export default function Artists() {
    useEffect(() => {
        // on click, moves you to the artists page
        document.body.addEventListener('click', () => {window.location.href = "./artists/"})
    });

    const longDesc = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In ultricies pellentesque lobortis. Etiam luctus neque volutpat enim pulvinar vulputate. Praesent rhoncus faucibus magna a venenatis.";
    return (
        <div className={"flex flex-row justify-center"}>
            <Artist name={"placeholder"} img={"/images/default-artist.png"} desc={"placeholder text"} rank={1}/>
            <Artist name={"placeholder"} img={"/images/default-artist.png"} desc={longDesc} rank={2}/>
        </div>
    );
}