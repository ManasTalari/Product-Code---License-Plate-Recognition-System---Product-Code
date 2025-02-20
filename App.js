import React, { useState,useEffect } from 'react';

const App = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  // useEffect(() => {
  //   const handleKeyDown = async (event) => {
  //     if (event.key === 's') {
  //       try {
  //         const response = await fetch('http://127.0.0.1:5000/save', {
  //           method: 'POST',
  //           body: null, // No need to send a body for a POST request
  //         });
  //         if (!response.ok) {
  //           throw new Error('Network response was not ok');
  //         }
  //         console.log('ROI saved successfully');
  //       } catch (error) {
  //         console.error('Error saving ROI:', error);
  //       }
  //     }
  //   };

  //   document.addEventListener('keydown', handleKeyDown);

  //   return () => {
  //     document.removeEventListener('keydown', handleKeyDown);
  //   };
  // }, []);
  const fetchData = () => {
    fetch('http://127.0.0.1:5000/save')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(jsonData => {
        setData(jsonData);
      })
      .catch(error => {
        setError(error);
      });
  };

  return (
    <div>
      <h1>Live Video Stream</h1>
      <img src="http://127.0.0.1:5000/video" alt="Live video" />
      <button onClick={fetchData}>save</button>
    </div>
  );
};

export default App;
