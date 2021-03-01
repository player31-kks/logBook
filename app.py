<<<<<<< HEAD

from flask import Flask, render_template, jsonify,request
from pymongo import MongoClient
import hashlib       
client = MongoClient('localhost', 27017) 
db = client.logbooks
=======
from pymongo import MongoClient
import jwt
import datetime
import hashlib
import secrets
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, escape
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
>>>>>>> 820c5021519669f9320a4ee342ced1d662e880b5

app = Flask(__name__)

app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'

# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
client = MongoClient('localhost', 27017)
db = client.LogBook

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('join.html')

# API 역할을 하는 부분
##login
@app.route('/api/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def login_set():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    print(username_receive,password_receive)

    result = db.users.find_one({'id': username_receive, 'pw': password_receive})


    if result is not None:
        
        session['user_id'] = username_receive

        print('%s' % escape(session['user_id']))

        return jsonify({'result': 'success'})

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
        return render_template('fail.html')
    name = request.form['name']
    birth = request.form['birth']
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    db.users.insert_one({
        "email" : email,
        "name" : name,
        "birth" : birth,
        "password" : password_hash
    })
    # return jsonify({"result":"success"})
    return render_template('success.html')

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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)