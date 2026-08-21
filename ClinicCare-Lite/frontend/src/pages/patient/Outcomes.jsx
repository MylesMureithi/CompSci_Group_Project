import Card from "../../components/common/Card";
import Button from "../../components/common/Button";

function Outcomes() {
  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Health Outcomes</h1>
          <p>Review the outcomes and feedback from your health assessments.</p>
        </div>
      </div>

      <div className="outcome-list">
        <Card>
          <div className="outcome-header">
            <div>
              <h2>General Health Assessment</h2>
              <span className="outcome-date">
                Reviewed: August 20, 2026
              </span>
            </div>

            <span className="status status-reviewed">Reviewed</span>
          </div>

          <div className="outcome-summary">
            <h3>Clinician Feedback</h3>
            <p>
              Your assessment has been reviewed. Your clinician has provided
              feedback and recommendations based on your responses.
            </p>
          </div>

          <Button variant="secondary">View Details</Button>
        </Card>

        <Card>
          <div className="outcome-header">
            <div>
              <h2>Wellness Questionnaire</h2>
              <span className="outcome-date">
                Submitted: August 18, 2026
              </span>
            </div>

            <span className="status status-pending">Awaiting Review</span>
          </div>

          <div className="outcome-summary">
            <h3>Status</h3>
            <p>
              Your submission has been received and is currently awaiting
              review by your clinician.
            </p>
          </div>

          <Button variant="secondary">View Submission</Button>
        </Card>
      </div>
    </div>
  );
}

export default Outcomes;