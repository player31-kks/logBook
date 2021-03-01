
from flask import Flask, render_template, jsonify,request
from pymongo import MongoClient
import hashlib       
client = MongoClient('localhost', 27017) 
db = client.logbooks

app = Flask(__name__)

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('join.html')

# API 역할을 하는 부분
##login
@app.route('/api/login', methods=['POST'])
def login():
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