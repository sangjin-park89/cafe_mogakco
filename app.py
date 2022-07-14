from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)

client = MongoClient(
    'mongodb+srv://byunjihye:asdf33@cluster0.qulah.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta2


# 메인페이지=카페목록페이지 보기
@app.route('/')
def home():
    return render_template('index.html')


# 지혜님 만드신 지도api 확인용 단독 html 라우팅
@app.route('/map')
def map():
    return render_template('map.html')


# 카페 목록 요청하는 api
@app.route('/cafe', methods=['GET'])
def show_cafe():
    data = list(db.cafeList.find({}, {'_id': False, 'lat': False, 'lng': False}))
    return jsonify({'data': data})


# 카페등록페이지 보기
@app.route('/cafe_plus')
def cafe():
    return render_template('cafePlus.html')


# 카페 등록하는 api
@app.route("/cafe", methods=["POST"])
def save_cafe():
    name = request.form['name']
    address = request.form['address']
    lat = request.form['lat']
    lng = request.form['lng']
    rating = request.form['rating']
    # 후기에서 입력, 저장된 점수 디비에서 불러오기..
    createdAt = datetime.now().strftime('%Y-%m-%d')
    
    doc = {
        'name': name,
        'address': address,
        'lat': lat,
        'lng': lng,
        'rating': float(rating),
        'createdAt': createdAt
    }

    db.cafeList.insert_one(doc)
    return jsonify({'msg': '모각코 추천 카페로 등록되었습니다.'})


# 특정카페 상세페이지 보기
@app.route('/cafe/<string:name>')
def show_detail(name: str):
    return render_template('review.html')


# 후기 목록 요청하는 api
@app.route('/cafe/<string:name>', methods=['GET'])
def detail_cafe(name: str):
    data = db.cafeList.find_one({'name': name}, {'_id': False, 'lat': False, 'lng': False})
    return jsonify({'data': data})


# 특정카페 후기 등록하는 api
@app.route("/cafe/<string:name>", methods=["POST"])
def save_comment(name: str):
    # userid = request.form['userid']
    usability = request.form['usability']
    soundmood = request.form['soundmood']
    price = request.form['price']
    comment = request.form['comment']
    createdAt = datetime.now().strftime('%Y-%m-%d')

    doc = {
        'name': name,
        # 'userid': userid,
        'usability':usability,
        'soundmood':soundmood,
        'price':price,
        'comment':comment,
        'createdAt': createdAt,
    }
    db.comment.insert_one(doc)
    return jsonify({'msg': '후기 등록 완료'})


# 정희님 담당쓰 건드리기가 무서워용



@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

SECRET_KEY = 'SPARTA'
@app.route('/')
def go_home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})




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




@app.route("/comment/<string:name>", methods=["POST"])
def save_comment(name: str):
    userid = request.form['userid']
    content = request.form['content']
    createdAt = datetime.now().strftime('%Y-%m-%d')

    doc = {
        'name': name,
        'userid': userid,
        'content': content,
        'createdAt': createdAt,
    }
    db.comment.insert_one(doc)
    return jsonify({'msg': '댓글 등록 성공'})

@app.route('/comment/<string:name>', methods=['GET'])
def get_comments(name: str):
    data = list(db.comment.find({'name': name}, {'_id': False}))
    return jsonify({'data': data})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
