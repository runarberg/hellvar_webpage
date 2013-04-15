import json
from datetime import date

import models

URLARG = "oftheday.urlarg"

oftheday = models.OfTheDay()

def index(environ, start_response):
    today = date.today()
    total_oftheday = len(oftheday.get(items=['id']))
    nr_oftheday = ((today.month + today.day) % total_oftheday) + 1 
    msg_oftheday = oftheday.fetch(items=['message'], 
                                  where={'id': nr_oftheday})
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [str(msg_oftheday['message'])]

def all(environ, start_response):
    otd = oftheday.get(items=['id', 'message'])
    otd_json = json.dumps(
            [dict([('id', int(msg['id'])), ('message', msg['message'])])
             for msg in otd])
    start_response('200 OK',
                   [('Content-Type', 'application/json; charset=UTF-8')])
    return [otd_json]
