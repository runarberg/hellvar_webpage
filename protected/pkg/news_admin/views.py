import os
import sys
import cgi
import re
from datetime import datetime
from sqlite3 import IntegrityError
sys.path.append("/home/protected/pkg")
sys.path.append("/home/sterna/Verkefni/Hellvar webpage/protected/pkg")

from jinja2 import Environment, FileSystemLoader
from markdown import markdown

from wsgi_app import security
from news import models

URLARG = "news_admin.urlargs"
news = models.News()

# Template support

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = Environment(loader=FileSystemLoader(template_dir),
                        autoescape=True)

def format_datetime(timestr):
    time = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
    return time.strftime("%d. %b %Y, %H:%M")
    
def markdown_filter(text):
    return markdown(text)
    
jinja_env.filters['datetime'] = format_datetime
jinja_env.filters['markdown'] = markdown_filter

# Handy helper functions

def render(template, *args, **kwargs):
    template = jinja_env.get_template(template)
    return [template.render(*args, **kwargs).encode('utf-8'), ]

def start_200(start_response):
    return start_response("200 OK", [("Content-Type", "text/html")])

def redirect(start_response, href):
    return start_response("301 Redirect", [("Location", href)])

def request_method(environ):
    return environ['REQUEST_METHOD']
    
def RequestForm(environ):
    return cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

def get_unicode_value(self, field):
    value = self.getvalue(field)
    try:
        unicode_value = value.decode('utf-8')
    except AttributeError:
        return value
    else:
        return unicode_value

setattr(cgi.FieldStorage, 'get_unicode_value', get_unicode_value)

def get_urlargs(environ, urlarg):
    return environ[urlarg]

# The Views

# /admin
def index(environ, start_response):    
    if request_method(environ) == "GET":
        posts = news.get(items=['id', 'title'])
        start_200(start_response)
    return render('index.html', **locals())

# /admin/posts/
def posts(environ, start_response):
    posts = news.get(items=['id', 'title', 'published', 'last_modified'])
    
    if request_method(environ) == "GET":
        start_200(start_response)
        
    elif request_method(environ) == "POST":
        form = RequestForm(environ)
        post_id = form.get_unicode_value('post_id')
        action = form.get_unicode_value('action')
        
        if post_id:
            if action == "delete":
                if isinstance(post_id, list):
                    for id in post_id:
                        news.delete(where={'id': id})
                else:
                    news.delete(where={'id': post_id})

                news.save()
                start_response('301 Redirect', [('Content-Type', 'text/html')])
                return render('redirect.html', href='posts')     

            elif action == "edit":
                if isinstance(post_id, basestring):
                    redirect(start_response, "{0}/edit".format(post_id))
                else:
                    select_to_many_error = True
                    start_200(start_response)

            elif action == "publish":
                time = datetime.now()
                if isinstance(post_id, list):
                    for id in post_id:
                        news.update(items={'published': time},
                                    where={'id': id})
                else:
                    news.update(items={'published': time},
                                where={'id': post_id})
                news.save()
                start_response('301 Redirect', [('Content-Type', 'text/html')])
                return render('redirect.html', href='posts')

            elif action == "unpublish":
                if isinstance(post_id, list):
                    for id in post_id:
                        news.update(items={'published': ''},
                                    where={'id': id})
                else:
                    news.update(items={'published': ''},
                                where={'id': post_id})
                news.save()
                start_response('301 Redirect', [('Content-Type', 'text/html')])
                return render('redirect.html', href='posts')     

        else:
            select_none_error = True
            start_200(start_response)
            
    return render('posts.html', **locals())
    
# /admin/posts/'post_id'/
def post_detail(environ, start_response):
    args = environ[URLARG]
    post_id = args[0]
    post = news.fetch(items=['id', 'text_body', 'title', 'published'],
                      where={'id': post_id})
    
    if request_method(environ) == 'GET':
        start_200(start_response)
        
    elif request_method(environ) == 'POST':
        if post['published']:
            # Unpublish by setting 'published' to empty string
            news.update(items={'published': ''}, where={'id': post_id})
            news.save()
        else:
            # Publish by setting the published time accordingly
            time = datetime.now()
            news.update(items={'published': time}, where={'id': post_id})
            news.save()

        start_response('301 Redirect', [('Content-Type', 'text/html')])
        return render('redirect.html', href='/posts/{0}'.format(post_id))
    
    return render('post_detail.html', **locals())
    
# /admin/new_post
def new_post(environ, start_response):
    if request_method(environ) == "GET":
        start_200(start_response)
        
    elif request_method(environ) == "POST":
        form = RequestForm(environ)
        title = form.get_unicode_value('title')
        text_body = form.get_unicode_value('text_body')
        time = datetime.now()

        try:
            news.insert(items={'title': title, 
                               'text_body': text_body,
                               'last_modified': time})
        except IntegrityError:
            not_unique_error = True
            start_200(start_response)
        else:
            news.save()
            post_id = news.fetch(items=['id'], where={'title': title})['id']
            redirect(start_response, '/posts/{0}'.format(post_id))
        
    return render('new_post.html', **locals())
    
# /admin/'post_id'/edit
def edit_post(environ, start_response):
    args = environ[URLARG]
    post_id = args[0]
    post = news.fetch(items=['id', 'title', 'text_body'],
                      where={'id': post_id})
    
    if request_method(environ) == "GET":
        start_200(start_response)
        
    elif request_method(environ) == "POST":
        form = RequestForm(environ)
        title = form.get_unicode_value('title')
        text_body = form.get_unicode_value('text_body')
        time = datetime.now()

        try:
            news.update(items={'title': title, 
                               'text_body': text_body,
                               'last_modified': time},
                               where={'id': post_id})
        except IntegrityError:
            not_unique_error = True
            start_200(start_response)
        else:
            news.save()
            redirect(start_response, "/posts/{0}".format(post_id))
        
    return render('edit_post.html', **locals())

# /admin/reset/
def reset_db(environ, start_response):
    if request_method(environ) == "GET":
        start_200(start_response)
        
    elif request_method(environ) == "POST":
        news.reset()
        news.save()
            
        redirect(start_response, '/')

    return render('reset.html', **locals())
    
# /admin/login/
def login(environ, start_response):
    if request_method(environ) == "GET":
        start_200(start_response)

    elif request_method(environ) == "POST":
        form = RequestForm(environ)
        user_id = form.get_unicode_value('user_id')
        password = form.get_unicode_value('password')
        authorized_users = [user.username for user in security.USERS]

        unhandled = True
        if user_id in authorized_users:
            # first get the correct user object
            user = filter(lambda x: x.username == user_id, security.USERS)[0]
            
            if password == user.password:
                # make user hash
                user_hash = security.make_secure_val(user_id.encode('utf-8'))
                start_response("301 Redirect",
                               [("Set-Cookie",
                                 "user_id={0}; Path=/".format(user_hash)),
                                ("Location", '/')])
                unhandled = False
                
        if unhandled:
            auth_error = True
            start_200(start_response)
    
    return render('login.html', **locals())

# /admin/logout/
def logout(environ, start_response):
    start_response("301 Redirect",
                   [("Set-Cookie", "user_id=; Path=/"),
                    ("Content-Type", 'text/html')])
    return render('redirect.html', href="/")

