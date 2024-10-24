import React, { useState,useRef } from "react";
import ParticlesBg from "particles-bg";
import Navigation from "./components/Navigation";
import Signin from "./components/Signin";
import Register from "./components/Register";
import FaceDetection from "./components/FaceDetection";
import Logo from "./components/Logo";
import ImageLinkForm from "./components/ImageLinkForm";
import Dashboard from "./components/Dashboard"; // Import Dashboard

const initialState = {
  input: "",
  imageURL: "",
  box: {},
  route: "signin", // Default route set to "signin"
  isSignedIn: false,
  user: {
    id: "",
    name: "",
    email: "",
    entries: 0,
    joined: "",
    image: null, // Store the image data from the backend
  },
};

const App = () => {
  const [state, setState] = useState(initialState);
  const clearImageRef = useRef(null); 

  // Clear Image when user signs out
  const clearImage = () => {
    if (clearImageRef.current) {
      clearImageRef.current(); // Call the clearImage function from ImageLinkForm
    }
    setState((prevState) => ({
      ...prevState,
      input: "",
      imageURL: "",
      box: {},
    }));
  };


  // Load User data after Signin/Register
  const loadUser = (data) => {
    setState((prevState) => ({
      ...prevState,
      user: {
        id: data._id,
        name: data.name,
        email: data.email,
        entries: data.entries,
        joined: data.joined,
        image: data.image || null, // Check if user has an image
      },
    }));


  };

  // Calculate face location for the detected faces
  const calculateFaceLocation = (data) => {
    const clarifaiFaces = data.outputs[0].data.regions.map(
      (region) => region.region_info.bounding_box
    );
    const image = document.getElementById("inputimage");
    const width = Number(image.width);
    const height = Number(image.height);

    const faceBoxes = clarifaiFaces.map((clarifaiFace) => {
      return {
        leftCol: clarifaiFace.left_col * width,
        topRow: clarifaiFace.top_row * height,
        rightCol: width - clarifaiFace.right_col * width,
        bottomRow: height - clarifaiFace.bottom_row * height,
      };
    });

    return faceBoxes;
  };

  const displayFaceBox = (boxes) => {
    setState((prevState) => ({ ...prevState, box: boxes }));
  };

  // Handle input change for the image URL
  const onInputChange = (event) => {
    setState((prevState) => ({ ...prevState, input: event.target.value }));
  };

  // Submit button logic to handle image submission
  const onButtonSubmit = () => {
    setState((prevState) => ({ ...prevState, imageURL: prevState.input }));
    // Further logic for submitting image and processing face detection
  };

  // Handle route change for navigation
  const onRouteChange = (route) => {
    if (route === "signout") {
      setState(initialState);
      clearImage(); // Clear image when signing out
    } else if (route === "home") {
      setState((prevState) => ({ ...prevState, isSignedIn: true, route: "home" }));
    } else if (route === "dashboard") {
      setState((prevState) => ({
        ...prevState,
        isSignedIn: true,
        route: "dashboard",
      }));
    } else {
      setState((prevState) => ({ ...prevState, route }));
    }
  };

  const { isSignedIn, imageURL, route, box, user } = state;

  return (
    <div className="App">
      <ParticlesBg type="cobweb" color="#f1ebeb" bg={true} />
      <Navigation isSignedIn={isSignedIn} onRouteChange={onRouteChange} />
      {route === "home" ? (
        <div>
          <ImageLinkForm
            onInputChange={onInputChange}
            onButtonSubmit={onButtonSubmit}
            onRouteChange={onRouteChange}
            userId={user.id}
            name={user.name}
            entries={user.entries}
            clearImageRef={clearImageRef} 
          />
          <FaceDetection box={box} imageURL={imageURL} clearImage={clearImage} />
        </div>
      ) : route === "signin" ? (
        <Signin loadUser={loadUser} onRouteChange={onRouteChange} />
      ) : route === "register" ? (
        <Register loadUser={loadUser} onRouteChange={onRouteChange} />
      ) : route === "dashboard" ? (
        <Dashboard userId={user.id} imageURL={user.image} />
      ) : (
        <Register loadUser={loadUser} onRouteChange={onRouteChange} />
      )}
    </div>
  );
};

export default App;
