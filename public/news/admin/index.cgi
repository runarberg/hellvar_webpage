#!/usr/bin/env python

import sys
sys.path.append("/home/protected/pkg")

from news_admin import application
from wsgi_app.middleware import ExceptionMiddleware, AuthMiddleware

# wrap the middlewares
application = AuthMiddleware(application, login_page='/login')
application = ExceptionMiddleware(application)      #for debugging
    
from wsgiref.handlers import CGIHandler
CGIHandler().run(application)
