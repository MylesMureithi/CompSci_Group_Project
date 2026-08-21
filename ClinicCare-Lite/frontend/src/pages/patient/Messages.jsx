import Card from "../../components/common/Card";
import Button from "../../components/common/Button";

function Messages() {
  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Messages</h1>
          <p>Communicate securely with your clinician.</p>
        </div>
      </div>

      <div className="message-layout">
        <Card className="conversation-list">
          <div className="message-section-header">
            <h2>Conversations</h2>
            <Button>New Message</Button>
          </div>

          <div className="conversation active">
            <div>
              <h3>Dr. Akoto</h3>
              <p>Your assessment has been reviewed.</p>
            </div>
            <span className="message-time">10:24 AM</span>
          </div>

          <div className="conversation">
            <div>
              <h3>ClinicCare Support</h3>
              <p>Welcome to ClinicCare.</p>
            </div>
            <span className="message-time">Yesterday</span>
          </div>
        </Card>

        <Card className="message-panel">
          <div className="message-panel-header">
            <div>
              <h2>Dr. Akoto</h2>
              <span>Clinician</span>
            </div>
          </div>

          <div className="messages">
            <div className="message received">
              <p>
                Your health assessment has been reviewed. Please let me know
                if you have any questions about the recommendations.
              </p>
              <span>10:20 AM</span>
            </div>

            <div className="message sent">
              <p>
                Thank you. I would like some clarification on the
                recommendations.
              </p>
              <span>10:24 AM</span>
            </div>
          </div>

          <div className="message-input">
            <input
              type="text"
              placeholder="Type your message..."
            />
            <Button>Send</Button>
          </div>
        </Card>
      </div>
    </div>
  );
}

export default Messages;