'use client';
import React, {useEffect} from 'react';
import Image from 'next/image';
import Heading2 from "@/app/Components/Heading2";

export default function Artists() {
    useEffect(() => {
        // on click, moves you to the artists page
        document.body.addEventListener('click', () => {window.location.href = "./artists/"})
    });

    const longDesc = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In ultricies pellentesque lobortis. Etiam luctus neque volutpat enim pulvinar vulputate. Praesent rhoncus faucibus magna a venenatis.";
    return (
        <>
            <div className={"flex flex-row items-center pb-5"}>
                <Image
                    src={"/default-artist.png"}
                    alt={"The default artist image. A stick figure."}
                    width={200}
                    height={200}
                    className={"pr-10"}
                />
                <h2 className={"text-7xl text-black lowercase"}>#1 Artist</h2>
            </div>
            <p className={"items-start"}>top artist information</p>
        </>
    );
}