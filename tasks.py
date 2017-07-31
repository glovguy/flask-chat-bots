import time
import os
from celery import Celery
import spacy
from bots.rails_client import RailsClient

celery_app = Celery('tasks', broker=os.environ['REDIS_URL'])
nlp = spacy.load('en')

@celery_app.task
def echo_bot_feed(data):
    print("Message received, data: ", data)
    reply_url = data.get('reply_url')[0]
    if data.get('style') == ['user']:
        msg_client = RailsClient(reply_url)
        time.sleep(3)
        msg_client.send_message('Hello from the bot inside your computer')
    return "Message received, data: {0}".format(data)

@celery_app.task
def sandwich_bot_feed(data):
    print("Sandwich bot! Message received: ", data)
    reply_url = data.get('reply_url')[0]
    sandw_similarity = nlp(unicode(data.body)).similarity(nlp(u'sandwich'))
    print("Sandwich similarity: ", sandw_similarity)
    if data.get('style') == ['user'] and sandw_similarity > 0.5:
        reply_msg = "Yes, that's a sandwich"
    else:
        reply_msg = "No, that's not a sandwich"
    msg_client = RailsClient(reply_url)
    msg_client.send_message(reply_msg)
    return "Message received, data: {0}".format(data)
