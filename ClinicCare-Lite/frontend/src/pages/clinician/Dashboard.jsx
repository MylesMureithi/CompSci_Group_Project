import { Link } from "react-router-dom";
import Card from "../../components/common/Card";
import Button from "../../components/common/Button";

function Dashboard() {
  return (
    <div className="dashboard">
      <section className="dashboard-header">
        <div>
          <h1>Clinician Dashboard</h1>
          <p>Here's an overview of your clinical activities.</p>
        </div>
      </section>

      <section className="dashboard-grid">
        <Card>
          <div className="card-header">
            <h2>Submissions</h2>
            <span className="card-count">8</span>
          </div>

          <p>8 patient submissions are awaiting your review.</p>

          <Link to="/clinician/submissions">
            <Button>View Submissions</Button>
          </Link>
        </Card>

        <Card>
          <div className="card-header">
            <h2>Health Forms</h2>
            <span className="card-count">4</span>
          </div>

          <p>Manage the health forms available to your patients.</p>

          <Link to="/clinician/forms">
            <Button>Manage Forms</Button>
          </Link>
        </Card>

        <Card>
          <div className="card-header">
            <h2>Reviews</h2>
            <span className="card-count">3</span>
          </div>

          <p>You have 3 reviews that require your attention.</p>

          <Link to="/clinician/reviews">
            <Button>View Reviews</Button>
          </Link>
        </Card>

        <Card>
          <div className="card-header">
            <h2>Messages</h2>
            <span className="card-count">5</span>
          </div>

          <p>You have 5 unread messages from patients.</p>

          <Link to="/clinician/messages">
            <Button>Open Messages</Button>
          </Link>
        </Card>
      </section>
    </div>
  );
}

export default Dashboard;