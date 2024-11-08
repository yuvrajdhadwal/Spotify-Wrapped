'use client';
import React from 'react';
import Heading1 from '../../Components/Heading1'
import { useEffect } from 'react';

export default function Title() {
    // links the entire page to the artist page
    useEffect(() => {
      document.body.addEventListener('click', () => {
        window.location.href = "./artists/";
      });
    }, []);
    return (
        <>
            <Heading1 text = "Let's see what we're working with..."/>
        </>
    );
}