import requests

class RailsClient(object):

    def __init__(self, url):
        self.url = url

    def send_message(self, message_text):
        r = self.post_message(message_text)
        print("posted!")
        print(r.status_code, r.reason)

    def post_message(self, message_text):
        msg_json={ 'data': { 'attributes': { 'body': '', 'sender': 2, 'style': 'bot' } } }
        msg_json['data']['attributes']['body'] = message_text
        message_url = str(self.url) + "/api/messages"
        return requests.post(message_url, json=msg_json)
