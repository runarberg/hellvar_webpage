import os, sys, cgi
sys.path.append("/home/protected/pkg")
sys.path.append("/home/sterna/Verkefni/Hellvar webpage/protected/pkg")

from jinja2 import Environment, FileSystemLoader

from wsgi_app import security
from oftheday import models

URLARG = 'oftheday_admin.urlarg'
oftheday = models.OfTheDay()

# Template support

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = Environment(loader=FileSystemLoader(template_dir),
                        autoescape=True)

# Helper functions

def start_200(start_response):
    return start_response('200 OK', [('Content-Type', 'text/html')])

def redirect(start_response, href):
    return start_response("301 Redirect", [("Location", href)])

def render(template, *args, **kwargs):
    template = jinja_env.get_template(template)
    return [str(template.render(*args, **kwargs)), ]

def request_method(environ):
    return environ['REQUEST_METHOD']

def RequestForm(environ):
    return cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

def get_urlargs(environ):
    return environ[URLARG]    

# The views

def index(environ, start_response):
    messages = oftheday.get(items=['id', 'message'])
    if request_method(environ) == 'GET':
        start_200(start_response)
    elif request_method(environ) == 'POST':
        form = RequestForm(environ)
        otd_id = form.getvalue('otd_id')
        action = form.getvalue('action')
        if otd_id:
            if action == "delete":
                if isinstance(otd_id, list):
                    for i in otd_id:
                        oftheday.delete(where={'id': i})
                else:
                    oftheday.delete(where={'id': otd_id})
                oftheday.save()

                start_response('301 Redirect', [('Content-Type', 'text/html')])
                return render('redirect_home.html')
            elif action == "edit":
                if not isinstance(otd_id, list):
                    redirect(start_response, "{0}/edit".format(otd_id))
                else:
                    select_tomany_error = True
                    start_200(start_response)
        else:
            select_none_error = True
            start_200(start_response)
        
    return render('index.html', **locals())

def reset_db(environ, start_response):
    if request_method(environ) == 'GET':
        start_200(start_response)
        
    elif request_method(environ) == 'POST':
        oftheday.reset()
        oftheday.save()

        redirect(start_response, '/')
        
    return render('reset.html', **locals())

def new_input(environ, start_response):
    if request_method(environ) == 'GET':
        start_200(start_response)

    elif request_method(environ) == 'POST':
        form = RequestForm(environ)
        message = form.getvalue('message')
        
        oftheday.insert(items={'message': message})
        oftheday.save()

        redirect(start_response, '/')
        
    return render('new.html', **locals())

def edit(environ, start_response):
    otd_id = get_urlargs(environ)[0]
    if request_method(environ) == 'GET':
        message = oftheday.fetch(items=['id', 'message'],
                                 where={'id': otd_id})
        start_200(start_response)

    elif request_method(environ) == 'POST':
        form = RequestForm(environ)
        message = form.getvalue('message')

        oftheday.update(items={'message': message},
                        where={'id': otd_id})
        oftheday.save()

        redirect(start_response, "/")

    return render('edit.html', **locals())

def login(environ, start_response):
    if request_method(environ) == 'GET':
        start_200(start_response)
        
    elif request_method(environ) == 'POST':
        form = RequestForm(environ)
        user_id = form.getvalue('user_id')
        password = form.getvalue('password')
        authorized_users = [user.username for user in security.USERS]

        unhandled = True
        if user_id in authorized_users:
            user = filter(lambda x: x.username == user_id, security.USERS)[0]
            if password == user.password:
                user_hash = security.make_secure_val(user_id)
                start_response("301 Redirect",
                               [("Set-Cookie",
                                 "user_id={0}; path=/".format(user_hash)),
                                ("Location", "/")])
                unhandled = False
        if unhandled:
            auth_error = True
            start_200(start_response)
        
    return render('login.html', **locals())

def logout(environ, start_response):
    start_response('301 Redirect', [("Set-Cookie", "user_id=; path=/")])
    return render('logout.html')
