from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///answers.db'
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)


# Define the model
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer1 = db.Column(db.String(200), nullable=False)
    answer2 = db.Column(db.String(200), nullable=False)
    answer3 = db.Column(db.String(200), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()
admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')
admin.add_view(ModelView(Answer, db.session))



# Define routes
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        answer1 = request.form['answer1']
        answer2 = request.form['answer2']
        answer3 = request.form['answer3']
        new_answer = Answer(
            question="User's Responses",
            answer1=answer1,
            answer2=answer2,
            answer3=answer3
        )
        db.session.add(new_answer)
        db.session.commit()
        return "Answers submitted successfully!"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
