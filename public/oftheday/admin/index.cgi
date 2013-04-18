#!/usr/bin/env python

import sys
sys.path.append("/home/protected/pkg")

from oftheday_admin import application
from wsgi_app.middleware import ExceptionMiddleware, AuthMiddleware

# wrap the middlewares
application = AuthMiddleware(application, login_page='/oftheday/admin/login')
application = ExceptionMiddleware(application)

if __name__ in '__main__':
    from wsgiref.handlers import CGIHandler
    CGIHandler().run(application)
