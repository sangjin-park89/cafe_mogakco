from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)
client = MongoClient(
    'mongodb+srv://test:sparta@cluster0.rf8ug.mongodb.net/?retryWrites=true&w=majority')
db = client.cafeMogakcoDB


@app.route('/')
def home():
    return render_template('index.html')


# 엄밀히는 보드(카페) 작성(등록) 페이지
@app.route('/boards')
def cafe():
    return render_template('boards.html')


# 카페 읽기 api
@app.route('/boards/list', methods=['GET']) # 왜 같은 라우트/boards는 안되나?
def show_cafe():
    cafes = list(db.cafe.find({}, {'_id': False}))
    # array = []
    # for 
    return jsonify({'all_cafe': cafes})
    # 이 녀석이 index.html에서 ajax GET 요청으로 DB 읽어온다


# 카페 등록 api = 이건 연습용 임시버전이고
# 실제론 지혜님이 지도api 통해 좌표 등 긁어서 db 저장 예정
@app.route('/boards', methods=['POST'])
def save_cafe():
    cafe_name_receive = request.form['cafe_name_give']
    cafe_address_receive = request.form['cafe_address_give']
    today = datetime.now()
    created_date = today.strftime('%Y-%m-%d')
    print(today)
    print(created_date)
    
    doc = {
        'cafe_name': cafe_name_receive,
        'cafe_address': cafe_address_receive,
        'date': created_date,
    }
    db.cafe.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


# 카페 후기 페이지
@app.route('/comments/<keyword>', methods=['GET', 'POST'])
def review(keyword):
# Q. keyword가 카페게시글의 id 이걸 어떻게 매칭해서 불러올지?
    comments = list(db.cafeReviews.find({}, {'_id': False}))
    # 여기서 모든 cafeReviews 말고 keyword 맞는거만!

    if request.method == "POST":
        # 후기작성 인풋에서 넘어오는 값들
        usability_receive = request.form['usability_give']
        sound_mood_receive = request.form['sound_mood_give']
        price_receive = request.form['price_give']
        comment_receive = request.form['comment_give']

        # 이 파일 여기서 은밀하게 저장할 값들
        today = datetime.now()
        created_date = today.strftime('%Y-%m-%d')
        cafe_ids = list(db.cafe.find({}, {'id':False}))

        doc = {
            # 'cafe_id': cafe_name_receive,
            # 'user_id': user_id,
            'usability': int(usability_receive),
            'sound_mood': int(sound_mood_receive),
            'price': int(price_receive),
            'comment': comment_receive,
            'date': created_date
        }
        db.cafeReviews.insert_one(doc)
        return jsonify({'msg': '저장 완료!'})
    else:
        return render_template('comments.html', keyword=keyword, comments=comments)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
