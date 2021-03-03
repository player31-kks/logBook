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
    print(coords)
    return render_template('main.html', coords = coords)

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
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

##join
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

##logbook
@app.route('/api/logbook', methods=['POST'])
def logbook_post():
    email_receive = request.form['username_give']
    num_receive = request.form['num_give']
    text_receive = request.form['text_give']
    src_receive = request.files['src_give']

    extension = src_receive.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{num_receive}-{mytime}'

    save_to = f'static/{filename}.{extension}'
    src_receive.save(save_to)

    db.users.insert_one({
        "email" : email_receive,
        "num" : num_receive,
        "text" : text_receive,
        "file" : f'{filename}.{extension}'
    })
    return jsonify({'result': True})

@app.route('/api/comment', methods=['POST'])
def comment_post():
    return render_template('login.html')

## logbook
@app.route('/logbook/<keyword>', methods=['GET'])
def todolist_get(keyword):
    token=request.cookies.get('token')
    payload=jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_info = db.users.find_one({'email' : payload['email']})
    
    if not user_info:
        return jsonify({'result' : False,'content' : "null",})
    
    logbook_info = db.logbook.find_one({'email':user_info['email'],'num':keyword})
    
    return jsonify({'result':True,'cotent':{
        'text' : logbook_info['text'],
        'src' : logbook_info['src']
    }})

@app.route('/api/todolist', methods=['POST'])
def todolist_post():
    return render_template('login.html')

if __name__ == '__main__':    
    app.run('0.0.0.0', port=5000, debug=True)