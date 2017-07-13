import requests

class RailsClient(object):

    def __init__(self):
        self.url = "http://localhost:3000/api/messages"

    @classmethod
    def send_message(cls, message_text):
        r = cls.post_message(message_text)
        print("posted!")
        print(r.status_code, r.reason)

    def post_message(message_text):
        msg_json={ 'data': { 'attributes': { 'body': '', 'sender': 2, 'style': 'bot' } } }
        msg_json['data']['attributes']['body'] = message_text
        return requests.post(self.url, json=msg_json)
