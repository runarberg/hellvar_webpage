#!/usr/bin/env python

import sys
sys.path.append("/home/protected/pkg")

from news import application
from wsgi_app.middleware import ExceptionMiddleware

# wrap the middlewares
application = ExceptionMiddleware(application)      #for debugging
    
from wsgiref.handlers import CGIHandler
CGIHandler().run(application)
