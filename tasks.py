import time
import os
from celery import Celery
from celery.bin import worker
import en_core_web_sm
from bots.chat_client import ChatClient
from bots.lib.bot_helper import *


celery_app = Celery('tasks', broker=os.environ['REDIS_URL'])
nlp = None


def load_nlp():
    global nlp
    if nlp is None:
        print("Loading nlp...")
        nlp = en_core_web_sm.load(tagger=None, parser=None, entity=None, matcher=None)


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
    chat_client = ChatClient(data)
    if nlp is None:
        chat_client.send_message("hmm...")
    load_nlp()
    SANDWICH = nlp('sandwich')
    print("Sandwich bot! Message received: ", data)
    if chat_client.last_sender() != 'user':
        return "Not replying, since message is not from user."
    comparison_text = chat_client.last_message()
    comparison_phrase = nlp(comparison_text)
    print("Phrase: {0}".format(comparison_phrase))
    sandw_similarity = comparison_phrase.similarity(SANDWICH)
    print("Sandwich word vector similarity: {0}".format(sandw_similarity))
    print("Is full sentence: {}".format(is_full_sentence(comparison_phrase)))

    if 'DYNO' not in os.environ:
        from nltk.corpus import wordnet
        WN_SANDWICH = wordnet.synset('sandwich.n.01')
        WN_ENTITY = wordnet.synset('entity.n.01')
        WN_FOOD = wordnet.synset('food.n.01')
        words = wordnet.synsets(comparison_text)
        if len(words) > 0:
            word = words[0]
            common_hypernyms = WN_SANDWICH.common_hypernyms(word)
        else:
            word = None
            common_hypernyms = []
        print("Synset matched: {0}".format(word))
        print("Common hypernyms: {0}".format(common_hypernyms))
        print("'DYNO' not in os.environ and common_hypernyms == [WN_ENTITY]: {0}".format('DYNO' not in os.environ and common_hypernyms == [WN_ENTITY]))

    if is_full_sentence(comparison_phrase):
        reply_msg = "beep boop, sorry I'm a dumb robot who doesn't understand full sentences"
    elif 'DYNO' not in os.environ and common_hypernyms == [WN_ENTITY]:
        reply_msg = "...that's not even a physical object"
    elif sandw_similarity > 0.85:
        reply_msg = "definitely a sandwich"
    elif 'DYNO' not in os.environ and WN_SANDWICH in common_hypernyms:
        reply_msg = "definitely a sandwich"
    elif sandw_similarity > 0.5:
        reply_msg = "yes, that's a sandwich"
    elif sandw_similarity == 0:
        reply_msg = "I don't know what that is"
    elif 'DYNO' not in os.environ and WN_FOOD in common_hypernyms:
        reply_msg = "I'd eat it, but it's not a sandwich"
    else:
        reply_msg = "no, that's not a sandwich"
    chat_client.send_message(reply_msg)
    return "Replying with: {0}".format(reply_msg)


if __name__ == '__main__':
    worker = worker.worker(app=celery_app)
    options = {
        'broker': os.environ['REDIS_URL'],
        'loglevel': 'INFO',
        'traceback': True,
        'concurrency': 1,
    }
    worker.run(**options)
