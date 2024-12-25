from flask import Flask, render_template, request, redirect, url_for, flash, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load student data from a JSON file
def load_students():
    with open('students.json', 'r') as f:
        return json.load(f)

students = load_students()
feedback_data = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matric_number = request.form['matric_number'].strip()
        surname = request.form['surname'].strip()

        # Validate matric number starts with "BMS"
        if not matric_number.startswith('BMS'):
            flash('Matric number must start with "BMS".', 'error')
            return render_template('login.html')

        # Validate credentials
        if matric_number in students and students[matric_number] == surname:
            session['user'] = matric_number
            return redirect(url_for('feedback'))
        else:
            flash('Invalid Matric Number or Surname!', 'error')

    return render_template('login.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        feedback = request.form['feedback']
        matric_number = session['user']
        feedback_data.append({'matric_number': matric_number, 'feedback': feedback})
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('success'))

    return render_template('feedback.html')

@app.route('/success')
def success():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('success.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
