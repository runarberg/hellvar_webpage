import sys, re
from traceback import format_tb
from Cookie import SimpleCookie

import security
from security import USERS

class ExceptionMiddleware (object):
    """Returns the exception in case of 500"""
    
    def __init__(self, app):
        self.app = app
        
    def __call__(self, environ, start_response):
        appiter = None
        
        try:
            appiter = self.app(environ, start_response)
            for item in appiter:
                yield item
        except:
            e_type, e_value, tb = sys.exc_info()
            traceback = ['Traceback (most recent call last):']
            traceback += format_tb(tb)
            traceback.append('{0}: {1}'.format(e_type.__name__, e_value))
            
            try:
                start_response('500 INTERNAL SERVER ERROR',
                               [('Content-Type', 'text/plain')])
            except:
                pass
            yield '\n'.join(traceback)
            
        if hasattr(appiter, 'close'):
            appiter.close()
            
class AuthMiddleware (object):
    authorized_users = [user.username for user in USERS]

    def __init__(self, app, login_page='/login'):
        self.app = app
        self.login_page = login_page

    def redirect_to_login(self, environ, start_response):
        # Prevent infinate redirection
        path = environ.get('PATH_INFO', '').lstrip('/')
        if path == self.login_page.lstrip('/'):
            return self.app(environ, start_response)
        else:
            start_response('301 REDIRECT',
                           [('Location', self.login_page)])
            return ['']
        
    def __call__(self, environ, start_response):
        cookie = SimpleCookie()
        try:
            cookie.load(environ['HTTP_COOKIE'])
            user_hash = cookie['user_id'].value
        except KeyError:
            # Not logged in, return to the login page
            return self.redirect_to_login(environ, start_response)
        else:
            user_id = security.check_secure_val(user_hash)
            if user_id and user_id in self.authorized_users:
                # valid user, continue
                # include user_id in the environ variable
                environ['app.user_id'] = user_id
                return self.app(environ, start_response)
            else:
                return self.redirect_to_login(environ, start_response)
