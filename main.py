from flask import Flask, jsonify, request
import tasks
import os
app = Flask(__name__)


@app.route('/post_test', methods=['POST'])
def hello_chat():
    data = dict(request.form)
    response = {
        'message': 'Message received by Flask-Chat-Bots',
        'status_code': "200 OK",}
    tasks.incoming_message.delay(data)
    return jsonify(response)


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
