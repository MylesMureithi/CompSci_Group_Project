import { useParams, Link } from "react-router-dom";
import Card from "../../components/common/Card";
import ReviewPanel from "../../components/clinician/ReviewPanel";

function Reviews() {
  const { id } = useParams();

  const submissions = {
    1: {
      patient: "Michael Johnson",
      form: "General Health Assessment",
      submitted: "August 20, 2026",
    },
    2: {
      patient: "Emma Williams",
      form: "Medication Information",
      submitted: "August 19, 2026",
    },
    3: {
      patient: "Daniel Smith",
      form: "Wellness Questionnaire",
      submitted: "August 18, 2026",
    },
    4: {
      patient: "Sarah Brown",
      form: "General Health Assessment",
      submitted: "August 17, 2026",
    },
  };

  const submission = submissions[id];

  if (!submission) {
    return (
      <div className="page">
        <Card>
          <h1>Submission Not Found</h1>
          <p>The requested submission could not be found.</p>

          <Link to="/clinician/submissions">
            Back to Submissions
          </Link>
        </Card>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header review-page-header">
        <div>
          <Link to="/clinician/submissions" className="back-link">
            ← Back to Submissions
          </Link>

          <h1>Review Submission</h1>
          <p>Review the patient's responses and provide feedback.</p>
        </div>
      </div>

      <Card>
        <ReviewPanel submission={submission} />
      </Card>
    </div>
  );
}

export default Reviews;