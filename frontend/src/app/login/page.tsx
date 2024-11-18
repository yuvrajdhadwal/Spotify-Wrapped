'use client';
import React from 'react';
import LoginForm from '../Components/LoginForm';
import Heading1 from '../Components/Heading1';

const login = () => {
  return (
    <div>
      <Heading1 text = {"Log Into Spotify Roaster"}/>
      <LoginForm />
    </div>
  );
};

export default login;
