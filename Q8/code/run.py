from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
from dotenv import load_dotenv
import os
load_dotenv()
API_SECRET = os.getenv('API_KEY')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    job_title = db.Column(db.String(120))
    feedback_text = db.Column(db.Text, nullable=False)
    def __repr__(self):
        return f"<Feedback {self.username}>"
@app.route('/')
def home():
    category = 'inspirational'
    api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'
    try:
        response = requests.get(api_url, headers={'X-Api-Key': API_SECRET})
        response.raise_for_status()
        resp = response.json()
        quote_of_the_day = resp[0]['quote'] if resp else "No quote available."
    except Exception as e:
        print(f"Error fetching quote: {e}")
        quote_of_the_day = "Error loading quote."
    feedbacks = Feedback.query.all()
    return render_template(
        'home.html',
        feedbacks=feedbacks,
        daily_quote=quote_of_the_day
    )
@app.route('/submit', methods=['POST'])
def submit_feedback():
    username = request.form.get('username')
    job_title = request.form.get('job_title')
    feedback_text = request.form.get('feedback')
    if not username or not feedback_text:
        return "Username and feedback are required!", 400
    new_feedback = Feedback(username=username, job_title=job_title, feedback_text=feedback_text)
    db.session.add(new_feedback)
    db.session.commit()
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True, port=5001)
