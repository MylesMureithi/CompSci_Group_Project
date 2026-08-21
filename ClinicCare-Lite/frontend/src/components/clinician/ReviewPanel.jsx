function ReviewPanel({ submission }) {
  return (
    <div className="review-panel">
      <div className="review-section">
        <h2>Patient Information</h2>

        <div className="patient-info">
          <div>
            <span>Name</span>
            <strong>{submission.patient}</strong>
          </div>

          <div>
            <span>Form</span>
            <strong>{submission.form}</strong>
          </div>

          <div>
            <span>Submitted</span>
            <strong>{submission.submitted}</strong>
          </div>
        </div>
      </div>

      <div className="review-section">
        <h2>Submission Responses</h2>

        <div className="response">
          <h3>How would you describe your general health?</h3>
          <p>Generally good, with occasional fatigue.</p>
        </div>

        <div className="response">
          <h3>Are you currently taking any medications?</h3>
          <p>Yes, I am currently taking prescribed medication.</p>
        </div>

        <div className="response">
          <h3>Do you have any current health concerns?</h3>
          <p>No major concerns at this time.</p>
        </div>
      </div>

      <div className="review-section">
        <h2>Clinician Feedback</h2>

        <textarea
          className="feedback-input"
          placeholder="Enter your feedback or recommendations..."
          rows="5"
        />
      </div>

      <div className="review-actions">
        <button className="button button-secondary">
          Save Draft
        </button>

        <button className="button button-success">
          Mark as Reviewed
        </button>
      </div>
    </div>
  );
}

export default ReviewPanel;