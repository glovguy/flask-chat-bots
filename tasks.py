import time
import os
from celery import Celery
import en_core_web_sm
from nltk.corpus import wordnet
from bots.chat_client import ChatClient

celery_app = Celery('tasks', broker=os.environ['REDIS_URL'])
nlp = en_core_web_sm.load()

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
        common_hypernyms = WN_SANDWICH.common_hypernyms(word)
    else:
        word = None
        common_hypernyms = []
    print("Synset matched: {0}".format(word))
    print("Common hypernyms: {0}".format(common_hypernyms))

    if sandw_similarity > 0.7 or WN_SANDWICH in common_hypernyms:
        reply_msg = "definitely a sandwich"
    elif sandw_similarity > 0.5:
        reply_msg = "yes, that's a sandwich"
    elif WN_FOOD in common_hypernyms:
        reply_msg = "I'd eat it, but it's not a sandwich"
    elif common_hypernyms == [WN_ENTITY]:
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
WN_FOOD = wordnet.synset('food.n.01')
