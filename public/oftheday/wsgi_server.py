import sys
sys.path.append("/home/sterna/Verkefni/Hellvar webpage/protected/pkg")

from oftheday import application
from wsgi_app.middleware import ExceptionMiddleware
from werkzeug.wsgi import SharedDataMiddleware

# wrap the middlewares
application = ExceptionMiddleware(application)      #for debugging
application = SharedDataMiddleware(application, {
    '/css': '/home/sterna/Verkefni/Hellvar webpage/public/css',
    '/js': '/home/sterna/Verkefni/Hellvar webpage/public/js'
})

if __name__ in '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1',
               8080,
               application,
               use_debugger=True,
               use_reloader=True)
