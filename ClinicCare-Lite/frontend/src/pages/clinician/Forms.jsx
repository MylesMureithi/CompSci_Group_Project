import Card from "../../components/common/Card";
import Button from "../../components/common/Button";

function Forms() {
  const forms = [
    {
      id: 1,
      name: "General Health Assessment",
      description: "Collect information about a patient's general health.",
      assigned: 24,
      status: "Active",
    },
    {
      id: 2,
      name: "Medication Information",
      description: "Collect information about current medications.",
      assigned: 18,
      status: "Active",
    },
    {
      id: 3,
      name: "Wellness Questionnaire",
      description: "Assess lifestyle, wellbeing, and general wellness.",
      assigned: 12,
      status: "Active",
    },
    {
      id: 4,
      name: "Follow-up Assessment",
      description: "Used for follow-up appointments and assessments.",
      assigned: 0,
      status: "Draft",
    },
  ];

  return (
    <div className="page">
      <div className="page-header forms-page-header">
        <div>
          <h1>Health Forms</h1>
          <p>Create and manage forms for your patients.</p>
        </div>

        <Button>Create Form</Button>
      </div>

      <div className="clinician-form-grid">
        {forms.map((form) => (
          <Card key={form.id}>
            <div className="clinician-form-header">
              <h2>{form.name}</h2>

              <span
                className={`status ${
                  form.status === "Active"
                    ? "status-active"
                    : "status-draft"
                }`}
              >
                {form.status}
              </span>
            </div>

            <p>{form.description}</p>

            <div className="form-stat">
              <span>Patients assigned</span>
              <strong>{form.assigned}</strong>
            </div>

            <div className="form-actions">
              <Button variant="secondary">Edit</Button>

              <Button>
                {form.status === "Draft" ? "Publish" : "View"}
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

export default Forms;