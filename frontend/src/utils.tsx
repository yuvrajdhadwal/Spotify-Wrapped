//import React, { useState, useEffect, ChangeEvent, FormEvent } from 'react';

// Helper function to get CSRF token from cookies
export function getCookie(name: string): string | null {
  const cookieValue = document.cookie
    .split('; ')
    .find((row) => row.startsWith(name + '='))
    ?.split('=')[1];
  return cookieValue ? decodeURIComponent(cookieValue) : null;
}