URLARG = 'oftheday_admin.urlarg'

def index(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['hello admiin',]

def login(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['login here',]
