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
    return render_template('main.html')

@app.route('/write')
def write():
    return render_template('write.html')


# @app.route('/listing_cafe', methods=['GET'])
# def show_cafe():
#     cafes = list(db.cafe_mogakco.find({}, {'_id': False}))
#     return jsonify({'all_cafe': cafes})


@app.route('/posting_cafe')
def cafe():
    return render_template('posting_cafe.html')

@app.route('/cafe', methods=['GET'])
def show_cafe():
    data = list(db.cafe.find({}, {'_id': False, 'lat': False, 'lng': False}))
    return jsonify({'data': data})

@app.route("/cafe", methods=["POST"])
def save_cafe():
    name = request.form['cafe_name']
    address = request.form['cafe_address']
    lat = request.form['lat']
    lng = request.form['lng']
    rating = request.form['rating']
    createdAt = datetime.now().strftime('%Y-%m-%d')

    doc = {
        'cafe_name': name,
        'cafe_address': address,
        'lat': lat,
        'lng': lng,
        'rating': rating,
        'createdAt': createdAt
    }

    db.cafe.insert_one(doc)

    return jsonify({'msg': '모각코GOGO 추천 카페로 등록되었습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
