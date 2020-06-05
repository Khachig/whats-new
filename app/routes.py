from flask import Flask, jsonify, request

from app import app

@app.route('/', methods=['GET'])
def home():
    return jsonify({'data': 'Hello World'})
