import { useState } from "react";
import { Link } from "react-router-dom";
import Button from "../components/common/Button";

function Login() {
  const [showPassword, setShowPassword] = useState(false);

  const [formData, setFormData] = useState({
    userId: "",
    password: "",
  });

  const [error, setError] = useState("");

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));

    setError("");
  }

  function handleSubmit(event) {
    event.preventDefault();

    if (!formData.userId || !formData.password) {
      setError("Please enter your user ID and password.");
      return;
    }

    // Backend authentication will be connected here.
    console.log("Login:", formData);
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-header">
          <h1>Welcome back</h1>
          <p>Log in to your ClinicCare account.</p>
        </div>

        {error && <div className="auth-error">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="userId">User ID</label>

            <input
              id="userId"
              name="userId"
              type="text"
              value={formData.userId}
              onChange={handleChange}
              placeholder="Enter your user ID"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>

            <div className="password-field">
              <input
                id="password"
                name="password"
                type={showPassword ? "text" : "password"}
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter your password"
              />

              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>
          </div>

          <Button type="submit">Log In</Button>
        </form>

        <p className="auth-footer">
          Don't have an account?{" "}
          <Link to="/register">Create one</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;