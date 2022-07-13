from fileinput import filename
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

# client = MongoClient('localhost', 27017)
client = MongoClient(
    'mongodb+srv://byunjihye:asdf33@cluster0.qulah.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta2
# 지혜님 몽고디비 연결해둠


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/map')
def cafe():
    return render_template('map.html')

@app.route('/cafe/<string:name>', methods=['GET'])
def detail_cafe(name: str):
    data = db.cafe.find_one({'name': name}, {'_id': False, 'lat': False, 'lng': False})
    return jsonify({'data': data})

@app.route('/cafe', methods=['GET'])
def show_cafe():
    data = list(db.cafe.find({}, {'_id': False, 'lat': False, 'lng': False}))
    return jsonify({'data': data})

@app.route("/cafe", methods=["POST"])
def save_cafe():
    name = request.form['name']
    address = request.form['address']
    lat = request.form['lat']
    lng = request.form['lng']
    rating = request.form['rating']
    createdAt = datetime.now().strftime('%Y-%m-%d')

    doc = {
        'name': name,
        'address': address,
        'lat': lat,
        'lng': lng,
        'rating': rating,
        'createdAt': createdAt
    }

    db.cafe.insert_one(doc)

    return jsonify({'msg': '모각코GOGO 추천 카페로 등록되었습니다.'})

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        "profile_info": ""                                          # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
