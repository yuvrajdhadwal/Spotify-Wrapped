'use client';
import React from 'react';
import SignupForm from '../Components/SignupForm';
import Heading1 from '../Components/Heading1';

const signup = () => {
  return (
    <div className={"flex flex-col items-center justify-center min-h-screen"}>
      <Heading1 text={"Sign up!"}></Heading1>
      <SignupForm />
    </div>
  );
};

export default signup;
