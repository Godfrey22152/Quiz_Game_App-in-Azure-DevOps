import os
import re
import random 
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_session import Session, MongoDBSessionInterface
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta


class MyMongoDBSessionInterface(MongoDBSessionInterface):
    def __init__(self, client, db, collection, key_prefix):
        self.store = client[db][collection]
        self.key_prefix = key_prefix

    def get_store_id(self, session):
        return self.key_prefix + session['f_sid']

    def get_mutable_dict(self, session):
        # Adjust as needed based on your session structure
        return dict(session)

    def save_session(self, app, session, response):
        store_id = self.get_store_id(session)
        data = self.get_mutable_dict(session)
        expiration = datetime.utcnow() + timedelta(minutes=app.config['PERMANENT_SESSION_LIFETIME'])
        self.store.update_one({'_id': store_id}, {'$set': {'data': data, 'expiration': expiration}}, upsert=True)


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Connect to MongoDB
client = MongoClient('mongodb://mongo:27017/')
db = client['quiz_app']
dumps_collection = db['dumps']
results_data_collection = db['results']
# Dictionary mapping quiz categories to their collections
quiz_collections = {
    'devOps': db['devOps_quizzes'],
    'current_affairs': db['current_affairs_quizzes'],
    'aws': db['aws_quizzes'],
    'azure': db['azure_quizzes']
}

# Dictionary mapping quiz categories to their questions collections
quiz_category_to_question_collections = {
    'devOps': db['devOps_questions'],
    'current_affairs': db['current_affairs_questions'],
    'aws': db['aws_questions'],
    'azure': db['azure_questions']
}

# Initialize Flask-Session
app.config['SESSION_TYPE'] = 'mongodb'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_USE_SIGNER'] = True  # Sign the session cookie for extra security
app.config['SESSION_KEY_PREFIX'] = 'quiz_app_'  # Replace with your desired prefix

# Use the custom MyMongoDBSessionInterface
mongo_session = MyMongoDBSessionInterface(client, db='quiz_app', collection='sessions', key_prefix='quiz_app_')
Session(app)


@app.route('/')
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'country' in request.form and 'education' in request.form and 'career' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        country = request.form['country']
        education = request.form['education']
        career = request.form['career']

        existing_account = db.accounts.find_one({'username': username})

        if existing_account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Name must contain only characters and numbers!'
        else:
            db.accounts.insert_one({
                'username': username,
                'password': password,
                'email': email,
                'country': country,
                'education': education,
                'career': career
            })
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('create_account.html', msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        account = db.accounts.find_one({'username': username, 'password': password})

        if account:
            session['loggedin'] = True
            session['id'] = str(account['_id'])
            session['username'] = account['username']
            msg = 'Logged in successfully!'
            return redirect(url_for('variety', msg=msg))
        else:
            msg = 'Incorrect username / password!'

    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    # Add a flag to indicate whether to show the "Return Home" button on the login page
    show_return_home = request.args.get('show_return_home', False)

    return render_template('login.html', msg='Logged out successfully!', show_return_home=True)

@app.route('/variety')
def variety():
    if 'loggedin' in session:
        msg = request.args.get('msg', '')  
        return render_template("variety.html", msg=msg)

    return redirect(url_for('login'))

@app.route('/dumps')
def dumps():
    dumps = dumps_collection.find()
    return render_template('dumps.html', dumps=dumps)


@app.route('/select_quiz', methods=['GET'])
def select_quiz():
    # Handle the GET request when a user clicks on a quiz link
    selected_quiz = request.args.get('selected_quiz')

    # Ensure the selected quiz category is valid
    if selected_quiz not in quiz_collections:
        return render_template('error.html', message='Invalid quiz selection')

    # Store the selected quiz category in the session
    session['selected_quiz'] = selected_quiz

    # Fetch quiz details from the chosen collection
    quiz_collection = quiz_collections[selected_quiz]
    quiz_details = quiz_collection.find()

    return render_template('select_quiz.html', quiz_details=quiz_details, selected_quiz=selected_quiz)

@app.route('/play_quiz/<string:quiz_id>')
def play_quiz(quiz_id):
    # Retrieve the last selected quiz category from the session
    selected_quiz = session.get('selected_quiz')

    if not selected_quiz:
        # Handle the case where no quiz category is found in the session
        abort(404, description="No quiz category selected.")

    # Check if the selected quiz category is valid
    quiz_collection = quiz_category_to_question_collections.get(selected_quiz)

    if not quiz_collection:
        abort(404, description=f"No quiz collection found for category '{selected_quiz}'.")

    # Fetch questions from the chosen collection using quiz_id
    questions = quiz_collection.find_one({'_id': ObjectId(quiz_id)})

    if not questions:
        abort(404, description=f"No quiz found with the ID '{quiz_id}' in category '{selected_quiz}'.")

    return render_template('play_quiz.html', questions=questions)


@app.route('/start_round/<string:quiz_id>', methods=['GET', 'POST'])
def start_round(quiz_id):

    selected_quiz = session.get('selected_quiz')

    quiz_collection = quiz_category_to_question_collections.get(selected_quiz)

    # Extract the 'questions' field from the document
    questions = quiz_collection.find_one({}).get('questions')  

    total_questions = len(questions)

    if not questions:
        flash(f"No questions found for the selected quiz.")
        return redirect(url_for('select_quiz'))

    # Shuffle the questions randomly
    random.shuffle(questions)

    # Initialize session variables
    session['questions'] = questions
    session['user_answers'] = [None] * len(questions)
    session['total_questions'] = total_questions

    # Redirect to the first question
    return redirect(url_for('question', question_num=1))


@app.route('/question/<int:question_num>', methods=['GET', 'POST'])
def question(question_num):
    questions = session.get('questions')
    total_questions = session.get('total_questions')

#   print(questions)
    if not questions:
        flash('No questions found.')
        return redirect(url_for('dumps'))

    if question_num <= 0 or question_num > len(questions):
        # Handle invalid question numbers by redirecting to the select quiz page
        flash('Invalid question number.')
        return redirect(url_for('select_quiz'))

    current_question_data = questions[question_num - 1]
    question_key = current_question_data['question']
    options_list = current_question_data['options']

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        user_answers = session.get('user_answers')
        user_answers[question_num - 1] = user_answer
        session['user_answers'] = user_answers
        next_question_num = question_num + 1

        if next_question_num > len(questions):
            return redirect(url_for('results'))

        return redirect(url_for('question', question_num=next_question_num))

    return render_template('question.html', question_num=question_num, question=question_key, options_list=options_list, total_questions=total_questions)

@app.route('/results')
def results():
    user_answers = session.get('user_answers')
    questions = session.get('questions')

    if user_answers is None or questions is None:
        flash('No answers found.')
        return redirect(url_for('index'))

    correct_answers = [q['correct_option'] for q in questions]

    correct_guesses, question_answer_pairs = check_answers(user_answers, correct_answers, questions)

    if len(correct_answers) == 0:
        score = 0
    else:
        score = int((correct_guesses / len(questions)) * 100)  

    total_correct = correct_guesses
    total_wrong = len(questions) - total_correct 

    results_data = []
    for question_num, (question, correct_ans, user_ans) in enumerate(question_answer_pairs, start=1):
        result = {
            'question_num': question_num,
            'question': question,
            'options': questions[question_num - 1]['options'],
            'correct_option': correct_ans,
            'user_guess': user_ans,
            'is_correct': correct_ans == user_ans
        }
        results_data.append(result)

    return render_template('results.html', score=score, results_data=results_data, total_correct=total_correct, total_wrong=total_wrong)


def check_answers(user_answers, correct_answers, questions):
    if len(user_answers) != len(correct_answers):
        return 0, []  

    correct_guesses = sum(1 for user_ans, correct_ans in zip(user_answers, correct_answers) if user_ans == correct_ans)

    question_answer_pairs = [(q['question'], correct_ans, user_ans) for q, correct_ans, user_ans in zip(questions, correct_answers, user_answers)]

    return correct_guesses, question_answer_pairs

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

