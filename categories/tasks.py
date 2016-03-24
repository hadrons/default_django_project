#coding: utf-8

from celery import Celery
from django.conf import settings

app = Celery('tasks', backend='amqp', broker=settings.BROKEN_URL)

@app.task
def print_hello():
    print 'hello there'