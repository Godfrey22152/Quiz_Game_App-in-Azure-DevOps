import os
import tempfile
import pytest
from flask import Flask
from pymongo import MongoClient
from app import app


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_quiz_app'
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(db_path)

def test_healthz(client):
    rv = client.get('/healthz')
    assert rv.status_code == 200
    assert rv.data == b'OK'

def test_ready(client):
    rv = client.get('/ready')
    assert rv.status_code == 200 or rv.status_code == 500

def test_welcome(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_create_account_get(client):
    rv = client.get('/create_account')
    assert rv.status_code == 200

def test_create_account_post(client):
    rv = client.post('/create_account', data={
        'username': 'testuser',
        'password': 'password',
        'email': 'testuser@example.com',
        'country': 'Testland',
        'education': 'Test University',
        'career': 'Test Engineer'
    })
    assert rv.status_code == 200
    assert b'You have successfully registered!' in rv.data or b'Account already exists!' in rv.data

def test_login_get(client):
    rv = client.get('/login')
    assert rv.status_code == 200

def test_login_post(client):
    rv = client.post('/login', data={
        'username': 'testuser',
        'password': 'password'
    })
    # Check if status code is 302 (redirect)
    assert rv.status_code == 302

    # Check if redirect location is correct
    redirect_url = rv.headers['Location']
    assert redirect_url.startswith('/variety')

    # Optionally, parse the query parameters and verify the success message
    from urllib.parse import urlparse, parse_qs
    parsed_url = urlparse(redirect_url)
    query_params = parse_qs(parsed_url.query)
    assert 'msg' in query_params
    assert query_params['msg'][0] == 'Logged in successfully!'
    
def test_logout(client):
    with client.session_transaction() as session:
        session['loggedin'] = True
    rv = client.get('/logout')
    assert rv.status_code == 200
    assert b'Logged out successfully!' in rv.data

def test_variety(client):
    with client.session_transaction() as session:
        session['loggedin'] = True
    rv = client.get('/variety')
    assert rv.status_code == 200

def test_select_quiz(client):
    with client.session_transaction() as session:
        session['loggedin'] = True
    rv = client.get('/select_quiz?selected_quiz=devOps')
    assert rv.status_code == 200 or rv.status_code == 404

def test_play_quiz(client):
    with client.session_transaction() as session:
        session['loggedin'] = True
        session['selected_quiz'] = 'devOps'
    rv = client.get('/play_quiz/64b81141d43eb338871cb1dd')
    assert rv.status_code == 200 or rv.status_code == 404

def test_start_round(client):
    with client.session_transaction() as session:
        session['loggedin'] = True
        session['selected_quiz'] = 'devOps'
    rv = client.get('/start_round/64b81141d43eb338871cb1dd')
    assert rv.status_code == 302  # Redirection to the first question

def test_question(client):
    with client.session_transaction() as session:
        session['loggedin'] = True
        session['questions'] = [{'question': 'test', 'options': ['a', 'b', 'c']}]
        session['total_questions'] = 1
    rv = client.get('/question/1')
    assert rv.status_code == 200

def test_results(client):
    with client.session_transaction() as session:
        session['loggedin'] = True
        session['user_answers'] = ['a']
        session['questions'] = [{'question': 'test', 'correct_option': 'a', 'options': ['a', 'b', 'c']}]
    rv = client.get('/results')
    assert rv.status_code == 200
