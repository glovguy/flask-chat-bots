import requests

class ChatClient(object):

    def __init__(self, data):
        self.data = data
        self.url = data.get('reply_url')[0]

    def last_sender(self):
        return self.data.get('style')[0]

    def last_message(self):
        return self.data.get('body')[0]

    def send_message(self, message_text):
        r = self.post_message(message_text)
        if r.status_code != 200:
            print("Error sending message to chat server")
            print(str(r.status_code) + ' ' + str(r.reason))

    def post_message(self, message_text):
        msg_json={ 'data': { 'attributes': { 'body': '', 'sender': 2, 'style': 'bot' } } }
        msg_json['data']['attributes']['body'] = message_text
        message_url = str(self.url) + "/api/messages"
        return requests.post(message_url, json=msg_json)