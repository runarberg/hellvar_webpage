URLARG = "oftheday.urlarg"

def index(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['this of the day',]
