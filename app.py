from pymongo import MongoClient
import jwt
import datetime
import hashlib
import secrets
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, escape
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
app = Flask(__name__)

app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'

# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
client = MongoClient('localhost', 27017)
db = client.LogBook

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/api/page', methods=['GET'])
def join():
    return render_template('join.html')
# API 역할을 하는 부분
#login
@app.route('/api/login', methods=['POST'])
def login_post():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    result = db.users.find_one({'email': username_receive, 'password': password_hash})
    print(result);

    if result is not None:
        
        payload = {
            'id': username_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds = 600)
        }
        print(payload)
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

    # 찾지 못하면   
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

    
    return render_template('login.html')

##join
@app.route('/api/signup', methods=['POST'])
def signup():
    email = request.form['email']
    exists = bool(db.users.find_one({'email':email}))
    if exists:
        # return jsonify({'result' : "id is already exist"})
        return jsonify({'result': 'fail', 'msg': '아이디가 이미 존재합니다.'})
    name = request.form['name']
    birth = request.form['birth']
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    doc = {
        "email" : email,
        "name" : name,
        "birth" : birth,
        "password" : password_hash
    }
    db.users.insert_one(doc)
    # return jsonify({"result":"success"})
    return jsonify({'result': 'success'})

## comment
@app.route('/api/comment', methods=['GET'])
def get_comment():
    return render_template('login.html')

@app.route('/api/comment', methods=['POST'])
def create_comment():
    return render_template('login.html')

## ToDolist
@app.route('/api/todolist', methods=['GET'])
def get_todolist():
    return render_template('login.html')

@app.route('/api/todolist', methods=['POST'])
def create_todolist():
    return render_template('login.html')


if __name__ == '__main__':    app.run('0.0.0.0', port=5000, debug=True)