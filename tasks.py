import time
import os
from celery import Celery
import spacy
from nltk.corpus import wordnet
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

    comparison_text = chat_client.last_message()
    comparison_phrase = nlp(comparison_text)
    print("Phrase: {0}".format(comparison_phrase))
    sandw_similarity = comparison_phrase.similarity(SANDWICH)
    print("Sandwich word vector similarity: {0}".format(sandw_similarity))

    words = wordnet.synsets(comparison_text)
    if len(words) > 0:
        word = words[0]
        lowest_c_hypernyms = WN_SANDWICH.lowest_common_hypernyms(word)
        if len(lowest_c_hypernyms) > 0:
            lowest_hyper = lowest_c_hypernyms[0]
        else:
            lowest_hyper = None
    else:
        word = None
        lowest_hyper = None
    print("Synset matched: {0}".format(word))
    print("Lowest common hypernym: {0}".format(lowest_hyper))

    if sandw_similarity > 0.5 or lowest_hyper is WN_SANDWICH:
        reply_msg = "yes, that's a sandwich"
    elif lowest_hyper is WN_ENTITY:
        reply_msg = "...that's not even a physical object"
    elif sandw_similarity == 0:
        reply_msg = "I don't know what that is"
    else:
        reply_msg = "no, that's not a sandwich"
    chat_client.send_message(reply_msg)
    return "Replying with: {0}".format(reply_msg)

SANDWICH = nlp(u'sandwich')
WN_SANDWICH = wordnet.synset('sandwich.n.01')
WN_ENTITY = wordnet.synset('entity.n.01')
