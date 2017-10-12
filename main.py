import os
import sys
import logging
from flask import Flask, jsonify, request
import tasks

app = Flask(__name__)
if 'DYNO' in os.environ:
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)
else:
    app.debug = True


@app.route('/')
def home_page():
    return "Welcome to Flask-Chat-Bots.\n\nFlask is running."

@app.route('/post_test', methods=['POST'])
def hello_chat():
    data = dict(request.form)
    sender = data.get('style')[0]
    if sender == 'user': tasks.echo_bot_feed.delay(data)
    return jsonify(MESSAGE_RECEIVED)

@app.route('/sandwich', methods=['POST'])
def sandwich_bot():
    data = dict(request.form)
    sender = data.get('style')[0]
    if sender == 'user': tasks.sandwich_bot_feed.delay(data)
    return jsonify(MESSAGE_RECEIVED)

MESSAGE_RECEIVED = {
        'message': 'Message received by Flask-Chat-Bots',
        'status_code': "200 OK",}

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5005))
    app.run(host='0.0.0.0', port=port)
