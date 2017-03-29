#!/usr/bin/env python

from flask import Flask, jsonify, render_template, Response, request
import json

app = Flask(__name__)
app.debug = True


@app.route('/')
def main_page():
    return render_template("index.html")


@app.route('/videoaction', methods=['POST'])
def receive_video_action():

    print('You are here!!')
    payload = (request.form)

    print(payload)

    resp = json.dumps(payload)
    return Response(resp, status=200, mimetype='application/json')


app.run(host='127.0.0.1', port=8083)
