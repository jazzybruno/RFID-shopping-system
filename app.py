from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import time
import serial
from functions import Card, play_audio, products
import sys
from functions import apiEndpoint, topUpEndpoint

app = Flask(__name__)


@app.route('/')
def activity():
    return render_template('activities.html')


@app.route('/topUp')
def topUp():
    return render_template('topUp.html')


@app.route('/purchase')
def index():
    products = [
        {"id": 1, "name": "Camera", "price": 30.99, "points": 100, "image_src": "./static/images/camera.png"},
        {"id": 2, "name": "Headset", "price": 59.99, "points": 150, "image_src": "./static/images/headset.png"},
        {"id": 3, "name": "HP ProBook", "price": 60.99, "points": 50, "image_src": "./static/images/hpprobook.png"},
        {"id": 4, "name": "MacBook Pro", "price": 84.99, "points": 120, "image_src": "./static/images/macbook.png"},
        {"id": 5, "name": "Play Station", "price": 44.99, "points": 120, "image_src": "./static/images/ps5.png"},
        {"id": 6, "name": "D-link Router", "price": 34.99, "points": 120, "image_src": "./static/images/router.png"},
        # Add more product objects here...
    ]
    return render_template('index.html', products=products)


@app.route('/success')
def success():
    message = request.args.get('message', 'Product processed successfully')
    return render_template('success.html', message=message)


@app.route('/error')
def error():
    message = request.args.get('message', 'An error occurred')
    return render_template('error.html', message=message)


@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        product = request.get_json()
        # Process the product object
        print(product)
        return apiEndpoint(product=product)


@app.route('/topPost', methods=['POST'])
def topUpPost():
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        print(amount)
        return topUpEndpoint(amount=amount)


if __name__ == '__main__':
    app.run()
