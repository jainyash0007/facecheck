import React, { useRef, useState, useEffect } from "react";
import Alert from "./Alert";

const ImageLinkForm = ({
  onInputChange,
  onRouteChange,
  name,
  userId,
  clearImageRef,
}) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [showAlert, setShowAlert] = useState(false);

  useEffect(() => {
    // Request camera access
    const enableCamera = async () => {
      try {
        const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
        setStream(mediaStream);
        if (videoRef.current) videoRef.current.srcObject = mediaStream;
      } catch (err) {
        console.error("Failed to enable camera: ", err);
      }
    };

    enableCamera();
    clearImageRef.current = clearImage;
    return () => {
      // Cleanup function to turn off the camera
      stream && stream.getTracks().forEach(track => track.stop());
    };
  }, []);

  const captureImage = () => {
    if (canvasRef.current && videoRef.current) {
      const context = canvasRef.current.getContext('2d');
  
      // Draw the current video frame onto the canvas
      context.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
  
      // Convert the canvas to a Blob and check if the blob is generated
      canvasRef.current.toBlob(blob => {
        if (!blob) {
          console.error("Failed to generate Blob from canvas.");
          return;
        }
  
        console.log("Generated Blob:", blob);
  
        const formData = new FormData();
        formData.append('image', blob);
        formData.append('userId', userId);
        formData.forEach((value, key) => {
          console.log(`${key}:`, value);
        });
  
        // Send the form data (image) to the server
        fetch(`${process.env.REACT_APP_SERVER}/upload-image`, {
          method: 'POST',
          body: formData
        })
        .then(response => {
          if (response.ok) {  // Check if the status is OK (200 or 201)
            return response.json();
          } else {
            throw new Error('Image upload failed');
          }
        })
        .then(data => {
          console.log("Image uploaded successfully:", data);
          onRouteChange("dashboard");
        })
        .catch(err => console.error("Error uploading image:", err));
      }, 'image/png');
    }
  };
  
  const clearImage = () => {
    if (videoRef.current) {
      videoRef.current.pause();
      setStream(null); // Ensure camera is turned off
    }
    setShowAlert(false);
  };

  const handleButtonSubmit = () => {
    if (!stream) {
      setShowAlert(true);
      return;
    }
    captureImage();
  };

  const handleCloseAlert = () => {
    setShowAlert(false);
  };

  return (
    <div className="container display">
      <div className="container">
        <h3 className="text-style">
          <h1>Welcome to Facecheck, {name}</h1>
        </h3>
        <div className="container" align="center">
          <video ref={videoRef} autoPlay playsInline width="640" height="480" />
          <canvas ref={canvasRef} style={{ display: 'none' }} width="640" height="480" />
          <br />
          <button onClick={handleButtonSubmit}>Capture Image</button>
        </div>
      </div>
      {showAlert && (
        <Alert
          message="Please enable the camera to capture image."
          onClose={handleCloseAlert}
        />
      )}
    </div>
  );
};

export default ImageLinkForm;
