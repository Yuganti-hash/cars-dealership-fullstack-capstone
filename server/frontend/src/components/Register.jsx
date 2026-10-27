import React, { useState } from "react";
import "./Register.css";

const Register = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const gohome = () => {
    window.location.href = window.location.origin;
  };

  const register = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    // Client-side validation
    if (!userName.trim() || !password || !firstName.trim() || !lastName.trim() || !email.trim()) {
      setError("All fields are required.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters long.");
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError("Please enter a valid email address.");
      return;
    }

    const register_url = window.location.origin + "/djangoapp/register";

    try {
      const res = await fetch(register_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userName: userName,
          password: password,
          firstName: firstName,
          lastName: lastName,
          email: email,
        }),
      });

      const json = await res.json();
      if (json.status === "Authenticated" || json.userName) {
        sessionStorage.setItem("username", json.userName || userName);
        setSuccess("Registration successful! Redirecting to home page...");
        setTimeout(() => {
          window.location.href = window.location.origin;
        }, 1500);
      } else if (json.error === "Already Registered") {
        setError("The username is already registered. Please use another username or log in.");
      } else {
        setError(json.error || "Registration failed. Please try again.");
      }
    } catch (err) {
      setError("Unable to connect to the server. Please check your network or try again later.");
    }
  };

  return (
    <div className="register_container">
      <div className="header_panel">
        <span className="title_text">Sign Up for Best Cars Dealership</span>
        <button type="button" className="close_btn" onClick={gohome}>✕</button>
      </div>

      <form className="register_form" onSubmit={register}>
        {error && <div className="error_message">{error}</div>}
        {success && <div className="success_message">{success}</div>}

        <div className="input_group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            placeholder="Username"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
            required
          />
        </div>

        <div className="input_row">
          <div className="input_group">
            <label htmlFor="firstName">First Name</label>
            <input
              type="text"
              id="firstName"
              name="firstName"
              placeholder="First Name"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
          </div>

          <div className="input_group">
            <label htmlFor="lastName">Last Name</label>
            <input
              type="text"
              id="lastName"
              name="lastName"
              placeholder="Last Name"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
          </div>
        </div>

        <div className="input_group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            placeholder="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="input_group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div className="submit_panel">
          <button className="btn_register" type="submit">Register</button>
        </div>

        <div className="login_redirect">
          Already have an account? <a href="/login">Log in here</a>
        </div>
      </form>
    </div>
  );
};

export default Register;
