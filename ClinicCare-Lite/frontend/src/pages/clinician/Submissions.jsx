import { Link } from "react-router-dom";
import Card from "../../components/common/Card";
import Button from "../../components/common/Button";

function Submissions() {
  const submissions = [
    {
      id: 1,
      patient: "Nigel Asante",
      form: "General Health Assessment",
      submitted: "August 20, 2026",
      status: "Pending Review",
    },
    {
      id: 2,
      patient: "Miles Morales",
      form: "Medication Information",
      submitted: "August 19, 2026",
      status: "Pending Review",
    },
    {
      id: 3,
      patient: "Papa Kojo",
      form: "Wellness Questionnaire",
      submitted: "August 18, 2026",
      status: "Reviewed",
    },
    {
      id: 4,
      patient: "Stephanie Abakah",
      form: "Medication Review",
      submitted: "August 17, 2026",
      status: "Pending Review",
    },
  ];

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Patient Submissions</h1>
          <p>Review health forms submitted by your patients.</p>
        </div>
      </div>

      <Card className="submission-card">
        <div className="table-container">
          <table className="submission-table">
            <thead>
              <tr>
                <th>Patient</th>
                <th>Form</th>
                <th>Submitted</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {submissions.map((submission) => (
                <tr key={submission.id}>
                  <td>{submission.patient}</td>
                  <td>{submission.form}</td>
                  <td>{submission.submitted}</td>

                  <td>
                    <span
                      className={`status ${
                        submission.status === "Reviewed"
                          ? "status-reviewed"
                          : "status-pending"
                      }`}
                    >
                      {submission.status}
                    </span>
                  </td>

                  <td>
                    <Link to={`/clinician/reviews/${submission.id}`}>
                      <Button variant="secondary">Review</Button>
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}

export default Submissions;