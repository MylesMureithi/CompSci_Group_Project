import { NavLink } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <NavLink to="/">ClinicCare</NavLink>
      </div>

      <div className="navbar-links">
        <NavLink to="/">Home</NavLink>
        <NavLink to="/patient">Patient</NavLink>
        <NavLink to="/clinician">Clinician</NavLink>
      </div>
    </nav>
  );
}

export default Navbar;