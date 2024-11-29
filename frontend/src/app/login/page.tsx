'use client';
import React from 'react';
import LoginForm from '../Components/LoginForm';
import Heading1 from '../Components/Heading1';

const login = () => {
  return (
    <div className={"flex flex-col items-center justify-center min-h-screen"}>
      <Heading1 text = {"Login to Spotify Roaster"}/>
      <LoginForm />
    </div>
  );
};

export default login;
