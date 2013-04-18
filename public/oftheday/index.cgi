#!/usr/bin/env python

import sys
sys.path.append("/home/protected/pkg")

from oftheday import application
from wsgi_app.middleware import ExceptionMiddleware

# wrap the middlewares
application = ExceptionMiddleware(application)

if __name__ in '__main__':
    from wsgiref.handlers import CGIHandler
    CGIHandler().run(application)
