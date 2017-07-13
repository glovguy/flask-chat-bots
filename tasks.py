import time
from celery import Celery
from bots.rails_client import RailsClient

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def incoming_message(data):
    print("Message received, data: ", data)
    if data.get('style') == ['user']:
        msg_client = RailsClient()
        time.sleep(3)
        msg_client.send_message('Hello from the bot inside your computer')
    return "Message received, data: {0}".format(data)
