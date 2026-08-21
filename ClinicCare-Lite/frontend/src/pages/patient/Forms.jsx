import Card from "../../components/common/Card";
import Button from "../../components/common/Button";

function Forms() {
  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Health Forms</h1>
          <p>Complete and submit the health forms assigned to you.</p>
        </div>
      </div>

      <div className="form-list">
        <Card>
          <div className="form-content">
            <div>
              <h2>General Health Assessment</h2>
              <p>
                Provide information about your general health and wellbeing.
              </p>
              <span className="form-meta">Estimated time: 5 minutes</span>
            </div>
          </div>

          <Button>Open Form</Button>
        </Card>

        <Card>
          <div className="form-content">
            <div>
              <h2>Medication Information</h2>
              <p>
                Provide information about medications you are currently taking.
              </p>
              <span className="form-meta">Estimated time: 3 minutes</span>
            </div>
          </div>

          <Button>Open Form</Button>
        </Card>

        <Card>
          <div className="form-content">
            <div>
              <h2>Wellness Questionnaire</h2>
              <p>
                Answer questions about your current lifestyle and wellbeing.
              </p>
              <span className="form-meta">Submitted: August 18, 2026</span>
            </div>
          </div>

          <Button variant="secondary">View Submission</Button>
        </Card>
      </div>
    </div>
  );
}

export default Forms;