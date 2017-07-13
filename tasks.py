import time
from celery import Celery
from bots.rails_client import RailsClient

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def incoming_message(data):
    print("Message received, data: ", data)
    if data.get('style') is ['user']:
        time.sleep(3)
        send_message('Hello from the bot inside your computer')
    return 'some message here'
