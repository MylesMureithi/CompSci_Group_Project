import Card from "../../components/common/Card";
import Button from "../../components/common/Button";

function Messages() {
  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Messages</h1>
          <p>Communicate securely with your patients.</p>
        </div>
      </div>

      <div className="message-layout">
        <Card className="conversation-list">
          <div className="message-section-header">
            <h2>Patients</h2>
            <Button>New Message</Button>
          </div>

          <div className="conversation active">
            <div>
              <h3>Michael Johnson</h3>
              <p>I have a question about my assessment.</p>
            </div>

            <span className="message-time">10:24 AM</span>
          </div>

          <div className="conversation">
            <div>
              <h3>Emma Williams</h3>
              <p>Thank you for your feedback.</p>
            </div>

            <span className="message-time">Yesterday</span>
          </div>

          <div className="conversation">
            <div>
              <h3>Sarah Brown</h3>
              <p>When should I complete my next assessment?</p>
            </div>

            <span className="message-time">Aug 19</span>
          </div>
        </Card>

        <Card className="message-panel">
          <div className="message-panel-header">
            <div>
              <h2>Michael Johnson</h2>
              <span>Patient</span>
            </div>
          </div>

          <div className="messages">
            <div className="message received">
              <p>
                I have a question about the recommendations from my health
                assessment.
              </p>

              <span>10:20 AM</span>
            </div>

            <div className="message sent">
              <p>
                Of course. Which recommendation would you like me to clarify?
              </p>

              <span>10:22 AM</span>
            </div>

            <div className="message received">
              <p>
                Could you explain the recommendation regarding my medication?
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