import os, sys, cgi, Cookie

from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import markdown as md

import db, models

URLARG = "news_admin.urlargs"

# Template support
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = Environment(loader=FileSystemLoader(template_dir),
                        autoescape=True)
def format_datetime(timestr):
    time = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
    return time.strftime("%d. %b %Y, %H:%M")
    
jinja_env.filters['datetime'] = format_datetime

# handy helper functions
def render(template, *args, **kwargs):
    template = jinja_env.get_template(template)
    return [str(template.render(*args, **kwargs)), ]

def start_200(start_response):
    return start_response("200 OK", [("Content-Type", "text/html")])

def redirect(start_response, href):
    return start_response("301 Redirect", [("Location", href)])

def request_method(environ):
    return environ['REQUEST_METHOD']
    
def RequestForm(environ):
    return cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)


# /admin
def index(environ, start_response):    
    if request_method(environ) == "GET":
        start_200(start_response)

    elif request_method(environ) == "POST":
        models.reset_posts()
            
        redirect(start_response, '/posts')

    return render('index.html', **locals())
    
# /admin/login/
def login(environ, start_response):
    if request_method(environ) == "GET":
        start_200(start_response)

    elif request_method(environ) == "POST":
        form = RequestForm(environ)
        user_id = form.getvalue('user_id')
        start_response("301 Redirect",
                       [("Set-Cookie", "user_id={0}; Path=/".format(user_id)),
                        ("Location", '/')])
    
    return render('login.html', **locals())

# /admin/logout/
def logout(environ, start_response):
    start_response("200 OK",
                   [("Set-Cookie", "user_id=; Path=/"),
                    ("Content-Type", 'text/html')])
    return render('logout.html', **locals())

# /admin/posts/
def posts(environ, start_response):
    if request_method(environ) == "GET":
        posts = db.get('id', 'title', 'published', 'last_modified')
        start_200(start_response)
        
    elif request_method(environ) == "POST":
        form = RequestForm(environ)
        post_id = form.getvalue('post_id')
        action = form.getvalue('action')
        
        if post_id and (action == "delete"):
            models.delete_posts(post_id)
            
        redirect(start_response, '/posts')
        
    return render('posts.html', **locals())
    
# /admin/post/'post_id'/
def post_detail(environ, start_response):
    args = environ[URLARG]
    post_id = args[0]
    post = db.fetch('id', 'text_body', 'title', 'published', id=post_id)
    
    if request_method(environ) == 'GET':
        post_display = md.markdown(post['text_body'])
        
        start_200(start_response)
        
    elif request_method(environ) == 'POST':
        if post['published']:
            models.unpublish_post(post_id)
        else:
            models.publish_post(post_id)

        redirect(start_response, '/posts')
    
    return render('post_detail.html', **locals())
    
# /admin/new_post
def new_post(environ, start_response):
    if request_method(environ) == "GET":
        start_200(start_response)
        
    elif request_method(environ) == "POST":
        form = RequestForm(environ)
        title = form.getvalue('title')
        text_body = form.getvalue('text_body')
        
        models.new_post(title, text_body)
        
        redirect(start_response, '/posts')
        
    return render('new_post.html', **locals())
    
# /admin/'post_id'/edit
def edit_post(environ, start_response):
    args = environ[URLARG]
    post_id = args[0]
    post = db.fetch('id', 'title', 'text_body', id=post_id)
    
    if request_method(environ) == "GET":
        start_200(start_response)
        
    elif request_method(environ) == "POST":
        form = RequestForm(environ)
        title = form.getvalue('title')
        text_body = form.getvalue('text_body')
        
        models.update_post(post_id, title, text_body)
        
        redirect(start_response, "/posts/{0}".format(post_id))
        
    return render('edit_post.html', **locals())