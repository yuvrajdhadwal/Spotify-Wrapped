'use client';
import React from 'react';
import Heading1 from '../Components/Heading1'
import Heading2 from '../Components/Heading2'

export default function Requests() {
    return (
        <>
            <Heading1 text = "Duo Requests"/>
            <Heading2 text={"Incoming"}/>
            <p>Incoming request data</p>
            <Heading2 text={"Outgoing"}/>
            <p>Outgoing request data</p>
        </>
    );
}