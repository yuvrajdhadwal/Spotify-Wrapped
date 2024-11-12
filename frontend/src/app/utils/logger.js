export function logError(message, error) {
    if (process.env.NODE_ENV === 'development') {
      console.error(message, error);
    }
  }
  
  export function logInfo(message, data) {
    if (process.env.NODE_ENV === 'development') {
      console.log(message, data);
    }
    // add functionality for external server when in production for this and error lolzer
  }
  