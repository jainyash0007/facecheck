import React, { useState, useEffect } from "react";

const Dashboard = ({ userId }) => {
  const [imageSrc, setImageSrc] = useState(null);

  useEffect(() => {
    // Fetch the image from the backend using the userId
    const fetchImage = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_SERVER}/get-image/${userId}`);
        if (!response.ok) {
          throw new Error("Image not found");
        }

        const blob = await response.blob(); // Convert the response to a blob (binary data)
        const imageUrl = URL.createObjectURL(blob); // Create a URL from the blob
        setImageSrc(imageUrl); // Set the image URL to state
      } catch (error) {
        console.error("Error fetching image:", error);
      }
    };

    if (userId) {
      fetchImage(); // Only fetch the image if a valid userId is provided
    }
  }, [userId]); // Fetch image whenever userId changes

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      {imageSrc ? (
        <img src={imageSrc} alt="User's Uploaded Image" />
      ) : (
        <p>No image found</p>
      )}
    </div>
  );
};

export default Dashboard;
