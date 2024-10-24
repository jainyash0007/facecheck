import React, { useState } from "react";
import Alert from "./Alert";

const Register = ({ loadUser, onRouteChange }) => {
  const [state, setState] = useState({
    email: "",
    password: "",
    name: "",
    cin: "",
    role: "student", // Default value for the dropdown
    showAlert: false,
    alertMessage: "",
  });

  const onNameChange = (event) => {
    const value = event.target.value;
    
    // Replace any character that is not a letter or space
    const filteredValue = value.replace(/[^a-zA-Z\s]/g, "");
  
    // Update the state with the filtered value (only letters and spaces)
    setState((prevState) => ({ ...prevState, name: filteredValue }));
  };

  const onEmailChange = (event) => {
    setState((prevState) => ({ ...prevState, email: event.target.value }));
  };

  const onPasswordChange = (event) => {
    setState((prevState) => ({ ...prevState, password: event.target.value }));
  };

  const onCinChange = (event) => {
    const value = event.target.value;

    // Ensure only numeric input and restrict max length to 9 characters
    if (/^\d*$/.test(value) && value.length <= 9) {
      setState((prevState) => ({ ...prevState, cin: value }));
    }
  };

  const onRoleChange = (event) => {
    setState((prevState) => ({ ...prevState, role: event.target.value }));
  };

  const handleCloseAlert = () => {
    setState((prevState) => ({
      ...prevState,
      showAlert: false,
      alertMessage: "",
    }));
  };

  const onSubmitSignIn = async () => {
    const { email, password, name, cin, role } = state;

    // Email domain validation
    if (!email || !email.includes("@") || !email.endsWith(".edu")) {
      setState((prevState) => ({
        ...prevState,
        showAlert: true,
        alertMessage: "Email must end with '.edu' to register.",
      }));
      return;
    }

    // Validate form fields
    if (!email || !password || !name || !cin || !role) {
      setState((prevState) => ({
        ...prevState,
        showAlert: true,
        alertMessage: "Please fill in all the fields.",
      }));
      return;
    }

    // Check for CIN and Email uniqueness
    try {
      const checkResponse = await fetch(`${process.env.REACT_APP_SERVER}/check-cin-email`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cin, email }),
      });

      // Ensure we handle non-JSON responses gracefully
      let checkData;
      try {
        checkData = await checkResponse.json();
      } catch (jsonError) {
        throw new Error("Server returned an invalid response. Please try again later.");
      }

      if (!checkResponse.ok) {
        throw new Error(checkData.message || "Error checking CIN and Email.");
      }

      // Check if either CIN or Email already exists
      if (checkData.emailExists) {
        setState((prevState) => ({
          ...prevState,
          showAlert: true,
          alertMessage: "Email already exists.",
        }));
        return;
      }
      if (checkData.cinExists) {
        setState((prevState) => ({
          ...prevState,
          showAlert: true,
          alertMessage: "CIN already exists.",
        }));
        return;
      }

      // Proceed with registration if both CIN and email are unique
      const registerResponse = await fetch(`${process.env.REACT_APP_SERVER}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          password,
          name,
          cin,
          role,  // Include the role in the request
        }),
      });

      // Handle non-JSON response or errors gracefully
      let registerData;
      try {
        registerData = await registerResponse.json();
      } catch (jsonError) {
        throw new Error("Server returned an invalid response during registration. Please try again.");
      }

      if (registerResponse.ok && registerData._id) {
        loadUser(registerData);
        onRouteChange("home");
      } else {
        throw new Error(registerData.message || "Registration failed. Please try again.");
      }
    } catch (error) {
      console.log("Error during registration:", error);
      setState((prevState) => ({
        ...prevState,
        showAlert: true,
        alertMessage: error.message || "Error during registration. Please try again.",
      }));
    }
  };

  return (
    <div className="container display">
      <div className="container homepage">
        <p className="heading">Register</p>
        <div className="container">
          <label className="form-title" htmlFor="name">Name</label>
          <br />
          <input
            className="input-area"
            type="text"
            name="name"
            id="name"
            value = {state.name}
            onChange={onNameChange}
          />
        </div>
        <div className="container">
          <label className="form-title" htmlFor="cin">CIN</label>
          <br />
          <input
            className="input-area"
            type="text"
            name="cin"
            id="cin"
            value={state.cin}
            onChange={onCinChange}
          />
        </div>
        <div className="container">
          <label className="form-title" htmlFor="role">Role</label>
          <br />
          <select
            className="input-area"
            name="role"
            id="role"
            value={state.role}
            onChange={onRoleChange}
          >
            <option value="student">Student</option>
            <option value="faculty">Faculty</option>
          </select>
        </div>
        <div className="container ">
          <label className="form-title" htmlFor="email-address">Email</label>
          <br />
          <input
            className="input-area"
            type="email"
            name="email-address"
            id="email-address"
            onChange={onEmailChange}
          />
        </div>
        <div className="container">
          <label className="form-title" htmlFor="password">Password</label>
          <br />
          <input
            className="input-area"
            type="password"
            name="password"
            id="password"
            onChange={onPasswordChange}
          />
        </div>
        <div>
          <button
            onClick={onSubmitSignIn}
            type="submit"
            value="Sign in"
            className="signin-button"
          >
            Register
          </button>
        </div>
        {state.showAlert && (
          <Alert message={state.alertMessage} onClose={handleCloseAlert} />
        )}
      </div>
    </div>
  );
};

export default Register;
