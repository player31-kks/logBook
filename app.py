from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)

SECRET_KEY = 'SPARTA'

client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
db = client.dbsparta_plus_week4

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('login.html')

# API 역할을 하는 부분
##login
@app.route('/api/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def login_set():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

    
    return render_template('login.html')

##join
@app.route('/api/signup', methods=['POST'])
def signup():
    return render_template('login.html')

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