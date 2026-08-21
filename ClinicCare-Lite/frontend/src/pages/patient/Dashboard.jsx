import { Link } from "react-router-dom";

import Card from "../../components/common/Card";
import Button from "../../components/common/Button";

function Dashboard() {
  return (
    <div className="dashboard">
      <section className="dashboard-header">
        <div>
          <h1>Welcome back</h1>
          <p>Here's an overview of your health activities.</p>
        </div>
      </section>

      <section className="dashboard-grid">
        <Card>
          <div className="card-header">
            <h2>Health Tasks</h2>
            <span className="card-count">3</span>
          </div>

          <p>You have 3 health tasks waiting for you.</p>

          <Link to="/patient/tasks">
            <Button>View Tasks</Button>
          </Link>
        </Card>

        <Card>
          <div className="card-header">
            <h2>Forms</h2>
            <span className="card-count">2</span>
          </div>

          <p>You have 2 forms available for submission.</p>

          <Link to="/patient/forms">
            <Button>View Forms</Button>
          </Link>
        </Card>

        <Card>
          <div className="card-header">
            <h2>Outcomes</h2>
            <span className="card-count">1</span>
          </div>

          <p>View your latest health assessment outcomes.</p>

          <Link to="/patient/outcomes">
            <Button>View Outcomes</Button>
          </Link>
        </Card>

        <Card>
          <div className="card-header">
            <h2>Messages</h2>
            <span className="card-count">2</span>
          </div>

          <p>You have 2 unread messages from your clinician.</p>

          <Link to="/patient/messages">
            <Button>Open Messages</Button>
          </Link>
        </Card>
      </section>
    </div>
  );
}

export default Dashboard;