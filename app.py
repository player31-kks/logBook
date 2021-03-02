from pymongo import MongoClient
import jwt
import datetime
import hashlib
import secrets
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, escape
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.LogBook

SECRET_KEY = 'SPARTA'

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('login.html')

##login

@app.route('/main', methods=['GET'])
def main_get():
    coords = list(db.imgcircle.find({},{'_id':False}))

    return render_template('main.html', coord = coords)

##login
@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def login_post():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'email': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'email': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

##signup

@app.route('/api/signup', methods=['POST'])
def signup_post():
    email = request.form['email']
    exists = bool(db.users.find_one({'email':email}))
    if exists:
        return jsonify({'result' : False})
        # return render_template('fail.html')

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
    
    return jsonify({"result":True})

@app.route('/api/duplicate', methods=['POST'])
def duplicate_post():
    email = request.form['email']
    exists = bool(db.users.find_one({"email": email}))
    if not exists:
        return jsonify({'result': True})
    return jsonify({'result': False})

## comment
@app.route('/api/comment', methods=['GET'])
def comment_get():
    num = request.form['num_give']
    all_comment = list(db.users.find({'num': num},{'_id':False}))
    return jsonify({'all_comment': all_comment})

@app.route('/api/comment', methods=['POST'])
def comment_post():
    email = request.form['username_give']
    num = request.form['num_give']    
    comment = request.form['comment_give']

    db.todolists.insert_one({
        "email" : email,
        "num" : num,
        "comment" : comment
    })
    return jsonify({'result': 'success'})

## ToDolist
@app.route('/api/todolist', methods=['GET'])
def todolist_get():
    num = request.form['num_give']
    all_text = list(db.users.find({'num': num},{'_id':False}))
    return jsonify({'all_text': all_text})

@app.route('/api/todolist', methods=['POST'])
def todolist_post():
    email = request.form['username_give']
    num = request.form['num_give']    
    text = request.form['text_give']

    db.todolists.insert_one({
        "email" : email,
        "num" : num,
        "text" : text
    })

    return jsonify({'result': 'success'})

if __name__ == '__main__':    app.run('0.0.0.0', port=5000, debug=True)