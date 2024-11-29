'use client';
import React from 'react';
import Image from 'next/image';
import Heading2 from "@/app/Components/Heading2";

export default function Artists() {
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