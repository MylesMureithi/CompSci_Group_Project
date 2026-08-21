import Card from "../../components/common/Card";
import Button from "../../components/common/Button";

function Tasks() {
  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Health Tasks</h1>
          <p>Complete the health tasks assigned to you.</p>
        </div>
      </div>

      <div className="task-list">
        <Card>
          <div className="task-content">
            <div>
              <h2>Health Assessment</h2>
              <p>Complete your general health assessment.</p>
              <span className="task-due">Due: August 25, 2026</span>
            </div>
          </div>

          <Button>Start Task</Button>
        </Card>

        <Card>
          <div className="task-content">
            <div>
              <h2>Medication Review</h2>
              <p>Review and confirm your current medications.</p>
              <span className="task-due">Due: August 28, 2026</span>
            </div>
          </div>

          <Button>Start Task</Button>
        </Card>

        <Card>
          <div className="task-content">
            <div>
              <h2>Wellness Questionnaire</h2>
              <p>Complete your monthly wellness questionnaire.</p>
              <span className="task-due">Completed: August 18, 2026</span>
            </div>
          </div>

          <Button variant="secondary">View Submission</Button>
        </Card>
      </div>
    </div>
  );
}

export default Tasks;