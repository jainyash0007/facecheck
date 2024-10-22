import React, { useRef, useState } from "react";
import Alert from "./Alert";

const ImageLinkForm = ({
  onInputChange,
  onButtonSubmit,
  name,
  entries,
  clearImage,
}) => {
  const inputRef = useRef(null);
  const [showAlert, setShowAlert] = useState(false);

  const clearInput = () => {
    clearImage();
    inputRef.current.value = "";
  };

  const handleButtonSubmit = () => {
    if (!inputRef.current.value) {
      setShowAlert(true);
    } else {
      onButtonSubmit();
    }
  };

  const handleCloseAlert = () => {
    setShowAlert(false);
  };

  return (
    <div className="container display">
      <div className="container">
        <h3 className="text-style">
          <h1>Welcome to Facecheck</h1>
        </h3>
        <div className="container" align="center">
          <input
            ref={inputRef}
            className="search-box"
            type="text"
            onChange={onInputChange}
            placeholder='Stay tuned for further updates'
          />
          <br />
        </div>
      </div>
      {showAlert && (
        <Alert
          message="Please enter the image link address."
          onClose={handleCloseAlert}
        />
      )}
    </div>
  );
};

export default ImageLinkForm;
