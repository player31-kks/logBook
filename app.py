from pymongo import MongoClient
import jwt
import datetime
import hashlib
import secrets
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, escape
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import json 
from bson import json_util

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.LogBook
SECRET_KEY = 'SPARTA'

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('login.html')
##email_get
@app.route('/api/get_email', methods=['GET'])
def email_get():
    token_receive = request.cookies.get('token')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return jsonify({"email":payload['email']})
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_get", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_get", msg="로그인 정보가 존재하지 않습니다."))

##main
@app.route('/main/<keyword>', methods=['GET'])
def main_get(keyword):
    token_receive = request.cookies.get('token')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        coords = list(db.imgcircle.find({},{'_id':False}))

        lokbook_list = list(db.logbook.find({'email':keyword},{'_id':False}).sort('num'))
        is_date = ['off' for i in range(len(coords))]
        for lokbook in lokbook_list:
            is_date[lokbook['num'] - 1] = 'on'
            
        for i in range(len(coords)):
            coords[i]['is_date'] = is_date[i]
        
        return render_template('main.html', coords = coords, email = keyword)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_get", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_get", msg="로그인 정보가 존재하지 않습니다."))

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
        # 'exp': datetime.utcnow() + timedelta(seconds= 5)  # 로그인 24시간 유지
        }
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
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
@app.route('/api/comment', methods=['POST'])
def comment_post():
    token_receive = request.cookies.get('token')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        email = payload['email']
        num_receive = request.form['comment']
        comment_receive = request.form['comment_give']

        db.users.insert_one({
            "email" : email,
            "num" : num_receive,
            "comment" : comment_receive,
        })
        return jsonify({'result': True})
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_get", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_get", msg="로그인 정보가 존재하지 않습니다."))

    return jsonify({'result': True})    

## logbook
@app.route('/logbook/<email>/<num>', methods=['GET'])
def logbook_get(email,num):
    try:
        token=request.cookies.get('token')
        payload=jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # user_info = db.users.find_one({'email' : payload['email']})
        # logbook_info = db.logbook.find({'email':user_info['email'],'num':int(keyword) })    
        log = list(db.logbook.find({},{'_id':False}))

        # num 이 현재페이지일 경우에만 새로운 리스트에 모아서 jinja 템플릿 보냄
        logbooks=[]
        for logs in log:
            if logs['num'] == int(num) and logs['email'] == email:
                logbooks.append(logs)
        if not logbooks:
            return render_template('logbook.html')
        else:
            return render_template('logbook.html',logbook=logbooks)

    except jwt.ExpiredSignatureError:
        return redirect('/')
    except jwt.exceptions.DecodeError:
        return redirect('/')
    except:
        return redirect('/') 

@app.route('/api/logbook', methods=['POST'])
def logbook_post():
    token_receive = request.cookies.get('token')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        email = payload['email']
        text_receive = request.form["text_give"]
        num_receive = request.form["num_give"]
        num = int(num_receive)
    
        file = request.files["file_give"]

        extension = file.filename.split('.')[-1]

        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

        filename = f'file-{mytime}'

        save_to = f'static/logbook_img/{filename}.{extension}'
        file.save(save_to)

        doc = {
            "email" : email,
            "num" : num,
            "text" : text_receive,
            "file" : f'{filename}.{extension}',
            "like" : 0
        }

        db.logbook.insert_one(doc)

        return jsonify({'msg':'저장 완료'})
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_get", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_get", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/api/logbook', methods=['DELETE'])
def logbook_delete():
    token_receive = request.cookies.get('token')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        email = request.form['email_give']
        num = request.form['num_give']
        file_name = request.form['file_give']

        # temp = db.logbook.find_one({'email': email, "file" : file_name, "num" : num})
        temp = db.logbook.find_one({'email':email})
        print(email, file_name, num)
        print(temp)
        # db.logbook.delete_one({'email': email, "file" : file_name, "num" : num})
        
        return jsonify({'msg': True})
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_get", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_get", msg="로그인 정보가 존재하지 않습니다."))
    except:
        return redirect(url_for("login_get", msg="error"))

##frined
@app.route('/api/friends', methods=['GET'])
def friend_get():
    token_receive = request.cookies.get('token')    
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        friend_list = list(db.friends.find({'email':payload['email']},{'_id':False}))
        return jsonify({'friend_list': friend_list})
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_get", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_get", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/api/friends', methods=['POST'])
def friend_post():
    token_receive = request.cookies.get('token')    
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        friends_email_receive = request.form['friends_email']
        
        already_friend = db.friends.find_one({'email':payload['email'],"friends_email" : friends_email_receive},{'_id':False})
        if already_friend:
            return jsonify({'result':'False','err':'이미 존재하는 친구입니다.'})
        
        user_info = db.users.find_one({'email' : friends_email_receive})
        if not user_info:
            return jsonify({'result': False ,'err':'친구 정보가 없습니다.'})
        else:
            db.friends.insert_one({
                "email" : payload['email'],
                "friends_email" : friends_email_receive,
            })
            return jsonify({'result': True, 'friend': friends_email_receive})
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_get", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_get", msg="로그인 정보가 존재하지 않습니다."))
    except:
        return redirect(url_for("login_get", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/api/friends', methods=['DELETE'])
def friend_delete():
    token_receive = request.cookies.get('token')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        friends_email_receive = request.form['friends_email_give']

        db.friends.remove({"email" : payload['email'], "friends_email" : friends_email_receive})
        return jsonify({'result': True})
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_get", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_get", msg="로그인 정보가 존재하지 않습니다."))

##like
@app.route('/api/like', methods=['GET'])
def like_get():
    token_receive = request.cookies.get('token')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return jsonify({'result': True})
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_get", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_get", msg="로그인 정보가 존재하지 않습니다."))
    except:
        return redirect(url_for("login_get", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/api/like', methods=['POST'])
def like_post():
    token_receive = request.cookies.get('token')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        email = request.form['email_give']
        num = request.form['num_give']
        file_name = request.form['file_give']

        target_logbook = db.logbook.find_one({'email': email, "file_name" : file_name, "num" : num})
        current_like = target_logbook['like']

        new_like = current_like + 1

        db.logbook.update_one({'email': email, "file_name" : file_name, "num" : num}, {'$set': {'like': new_like}})
        
        return jsonify({'result': True})
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_get", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_get", msg="로그인 정보가 존재하지 않습니다."))
    except:
        return redirect(url_for("login_get", msg="로그인 정보가 존재하지 않습니다."))

if __name__ == '__main__':    
    app.run('0.0.0.0', port=5000, debug=True)