import sys
sys.path.append("/home/sterna/Verkefni/Hellvar webpage/protected/pkg")

from news import application
from wsgi_app.middleware import ExceptionMiddleware

# wrap the middlewares
application = ExceptionMiddleware(application)      #for debugging

if __name__ in '__main__':
    from wsgiref.simple_server import make_server
    print "Serving on 127.0.0.1:8080"
    server = make_server('localhost', 8080, application)
    server.serve_forever()
