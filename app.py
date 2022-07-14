from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)
client = MongoClient(
    'mongodb+srv://byunjihye:asdf33@cluster0.qulah.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta2

# 메인페이지=카페목록페이지 보기
@app.route('/')
def home():
    return render_template('index.html')

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
        'name': name, # 디비에 저장하려는 카페이름 name으로 /cafe/<string:name>의 스트링네임을 어떻게 넣는지?
        # 그냥 이 상태로는 정의가 안 되어있다고 안되더라구요ㅜㅜ
        # 'userid': userid,
        # Q. 현재 로그인된 사람만 후기 작성 가능하니 로그인 된 user정보를 어떻게 작성자로 넣어야하는지?
        # 네비바에 예를 들어 ㅇㅇㅇ님 환영합니다 같은 곳이 있어야하고, 그 요소 값으로 끌어다 넣어야하는지?
        'usability':usability,
        'soundmood':soundmood,
        'price':price,
        'comment':comment,
        'createdAt': createdAt,
    }
    db.comment.insert_one(doc)
    return jsonify({'msg': '후기 등록 완료'})


# 후기 목록 요청하는 api
@app.route('/cafe/<string:name>', methods=['GET'])
def detail_cafe(name: str):
    data = db.cafeList.find_one({'name': name}, {'_id': False, 'lat': False, 'lng': False})
    return jsonify({'data': data})


# # 카페 후기 페이지
# @app.route('/comments/<keyword>', methods=['GET', 'POST'])
# def review(keyword):
# # Q. keyword가 카페게시글의 id 이걸 어떻게 매칭해서 불러올지?
#     comments = list(db.cafeReviews.find({}, {'_id': False}))
#     # 여기서 모든 cafeReviews 말고 keyword 맞는거만!

#     if request.method == "POST":
#         # 후기작성 인풋에서 넘어오는 값들
#         usability_receive = request.form['usability_give']
#         sound_mood_receive = request.form['sound_mood_give']
#         price_receive = request.form['price_give']
#         comment_receive = request.form['comment_give']

#         # 이 파일 여기서 은밀하게 저장할 값들
#         today = datetime.now()
#         created_date = today.strftime('%Y-%m-%d')
#         cafe_ids = list(db.cafe.find({}, {'id':False}))

#         doc = {
#             # 'cafe_id': cafe_name_receive,
#             # 'user_id': user_id,
#             'usability': int(usability_receive),
#             'sound_mood': int(sound_mood_receive),
#             'price': int(price_receive),
#             'comment': comment_receive,
#             'date': created_date
#         }
#         db.cafeReviews.insert_one(doc)
#         return jsonify({'msg': '저장 완료!'})
#     else:
#         return render_template('comments.html', keyword=keyword, comments=comments)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
