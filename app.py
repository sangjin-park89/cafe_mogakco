from fileinput import filename
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

# client = MongoClient('localhost', 27017)
client = MongoClient(
    'mongodb+srv://test:sparta@cluster0.rf8ug.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta
# db = client.dbsparta_plus_week1


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/listing_cafe', methods=['GET'])
def show_cafe():
    cafes = list(db.cafe_mogakco.find({}, {'_id': False}))
    return jsonify({'all_cafe': cafes})


@app.route('/posting_cafe')
def cafe():
    return render_template('posting_cafe.html')


@app.route('/posting_cafe', methods=['POST'])
def save_cafe():
    cafe_name_receive = request.form['cafe_name_give']
    cafe_address_receive = request.form['cafe_address_give']
    today = datetime.now()
    created_date = today.strftime('%Y-%m-%d')

    doc = {
        'cafe_name': cafe_name_receive,
        'cafe_address': cafe_address_receive,
        'date': created_date
    }
    db.cafe_mogakco.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
