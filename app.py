from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///responses.db'  # SQLite database
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_COOKIE_NAME'] = 'your_session_cookie'

db = SQLAlchemy(app)

# Create a model for the questionnaire responses
class QuestionnaireResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_1 = db.Column(db.Text, nullable=False)
    question_2 = db.Column(db.Text, nullable=False)
    question_3 = db.Column(db.Text, nullable=False)
    question_4 = db.Column(db.String(100), nullable=False)
    question_5 = db.Column(db.String(100), nullable=False)
    question_6 = db.Column(db.String(100), nullable=False)
    question_7 = db.Column(db.String(100), nullable=False)
    question_8 = db.Column(db.Text, nullable=False)
    question_9 = db.Column(db.Text, nullable=False)
    question_10 = db.Column(db.Text, nullable=False)
    question_11 = db.Column(db.Text, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Define the route to display the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the form data
        response = QuestionnaireResponse(
            question_1=request.form['question_1'],
            question_2=request.form['question_2'],
            question_3=request.form['question_3'],
            question_4=request.form['question_4'],
            question_5=request.form['question_5'],
            question_6=request.form['question_6'],
            question_7=request.form['question_7'],
            question_8=request.form['question_8'],
            question_9=request.form['question_9'],
            question_10=request.form['question_10'],
            question_11=request.form['question_11']
        )
        
        # Save the response to the database
        db.session.add(response)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('index.html')

# Define formatters for Flask-Admin to show readable labels instead of values
def format_question_4(view, context, model, name):
    choices = {
        'po4': 'Po, shpesh',
        'rralle4': 'Rrallë',
        'jo4': 'Jo'
    }
    return choices.get(model.question_4, 'Unknown')

def format_question_5(view, context, model, name):
    choices = {
        'po5': 'Po, mund të përdoret pa problem',
        'jo5': 'Jo, mund të përdoret vetëm në këtë strukturë',
        'nuk5': 'Nuk jam i sigurt'
    }
    return choices.get(model.question_5, 'Unknown')

def format_question_6(view, context, model, name):
    choices = {
        'po6': 'Po, ka ndodhur shpesh',
        'poka6': 'Po, ka ndodhur ndonjëherë',
        'jo6': 'Jo'
    }
    return choices.get(model.question_6, 'Unknown')

def format_question_7(view, context, model, name):
    choices = {
        'po7': 'Po, janë të informuar plotësisht',
        'jo7': 'Jo, duhet më shumë informacion',
        'nuk7': 'Nuk kam informacion të mjaftueshëm'
    }
    return choices.get(model.question_7, 'Unknown')

# Set up Flask-Admin for the admin interface
class QuestionnaireResponseAdmin(ModelView):
    column_formatters = {
        'question_4': format_question_4,
        'question_5': format_question_5,
        'question_6': format_question_6,
        'question_7': format_question_7,
    }

admin = Admin(app, name='Questionnaire Admin', template_mode='bootstrap3')
admin.add_view(QuestionnaireResponseAdmin(QuestionnaireResponse, db.session))

if __name__ == '__main__':
    app.run(debug=True)
