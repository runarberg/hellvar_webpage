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
    start_response('200 OK', [('Content-Type', 'text/plain; charset=UTF-8')])
    return [msg_oftheday['message'].encode('utf-8')]

def all(environ, start_response):
    otd = oftheday.get(items=['id', 'message'])
    otd_json = json.dumps(
        [dict([('id', int(msg['id'])), ('message', msg['message'])])
            for msg in otd],
        ensure_ascii=False
        )
    start_response('200 OK',
                   [('Content-Type', 'application/json; charset=UTF-8')])
    return [otd_json.encode('utf-8')]
