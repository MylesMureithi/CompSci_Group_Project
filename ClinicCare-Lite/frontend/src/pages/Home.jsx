import { Link } from "react-router-dom";
import Button from "../components/common/Button";

function Home() {
  return (
    <div className="home">
      <section className="hero">
        <div className="hero-content">
          <span className="hero-label">Healthcare Management Platform</span>

          <h1>
            Better healthcare,
            <br />
            connected through ClinicCare.
          </h1>

          <p>
            ClinicCare makes it easier for patients and clinicians to manage
            health tasks, forms, submissions, outcomes, and communication in
            one place.
          </p>

          <div className="hero-actions">
            <Link to="/login">
              <Button>Log In</Button>
            </Link>

            <Link to="/register">
              <Button variant="secondary">Create Account</Button>
            </Link>
          </div>
        </div>

        <div className="hero-visual">
          <div className="hero-card">
            <div className="hero-card-header">
              <span>ClinicCare</span>
              <span className="hero-status">● Active</span>
            </div>

            <div className="hero-card-content">
              <div className="hero-stat">
                <strong>📊 Health Tasks</strong>
              </div>

              <div className="hero-stat">
                <strong>📝 Forms</strong>

              </div>

              <div className="hero-stat">
                <strong>💬 Messages</strong>

              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="home-features">
        <div>
          <h2>For Patients</h2>
          <p>
            Complete assigned health tasks, submit forms, review outcomes,
            and communicate with your clinician.
          </p>
        </div>

        <div>
          <h2>For Clinicians</h2>
          <p>
            Manage health forms, review patient submissions, provide feedback,
            and communicate securely with patients.
          </p>
        </div>
      </section>
    </div>
  );
}

export default Home;