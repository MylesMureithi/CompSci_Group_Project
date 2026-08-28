from flask import Flask, render_template, request, session, redirect, url_for
import json
import bcrypt
from models.user import User
from models.health_task import HealthTask
from models.task_submission import TaskSubmission
from utils.email_handler import send_email

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form['user_id']
    password = request.form['password']
    with open('data/users.json', 'r') as f:
        users = json.load(f)
    
    # Check plain text password for testing
    if user_id in users and users[user_id]['password'] == password:
        session['user_id'] = user_id
        session['role'] = users[user_id]['role']
        return redirect(url_for('dashboard'))
    return render_template('login.html', error='Invalid credentials')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    role = session['role']
    
    if role == 'clinician':
        # Mock clinic data and clinician name
        clinician_name = session['user_id'] # Or pull from your users JSON
        clinic_data = {
            "clinic_id": "CLN-101",
            "name": "Ashesi Outpatient Health Centre",
            "assigned_clinician_id": session['user_id'],
            "registered_patients": [
                {"id": "PAT-901", "name": "Papa Kojo", "status": "Active"},
                {"id": "PAT-902", "name": "Myles Mureithi", "status": "Active"},
                {"id": "PAT-903", "name": "Stephanie Abakah", "status": "Active"}
            ]
        }
        return render_template('clinician_dashboard.html', name=clinician_name, clinic=clinic_data)
        
    return render_template('patient_dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)