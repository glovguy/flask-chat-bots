import time
import os
from celery import Celery
import spacy
from bots.chat_client import ChatClient

celery_app = Celery('tasks', broker=os.environ['REDIS_URL'])
nlp = spacy.load('en')

@celery_app.task
def echo_bot_feed(data):
    print("Message received, data: ", data)
    reply_url = data.get('reply_url')[0]
    if data.get('style') == ['user']:
        msg_client = ChatClient(data)
        time.sleep(3)
        msg_client.send_message('Hello from the bot inside your computer')
        return "Replied with an echo."
    else:
        return "No echo sent."

@celery_app.task
def sandwich_bot_feed(data):
    print("Sandwich bot! Message received: ", data)
    chat_client = ChatClient(data)
    if chat_client.last_sender() != 'user':
        return "Not replying, since message is not from user."
    word = nlp(chat_client.last_message())[0]
    print("Word: {0}".format(word))
    sandw_similarity = word.similarity(SANDWICH)
    print("Sandwich similarity: {0}".format(sandw_similarity))
    if sandw_similarity > 0.5:
        reply_msg = "Yes, that's a sandwich"
    else:
        reply_msg = "No, that's not a sandwich"
    chat_client.send_message(reply_msg)
    return "Replying with: {0}".format(reply_msg)

SANDWICH = nlp(u'sandwich')[0]
