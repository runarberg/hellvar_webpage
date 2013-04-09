import os, sys, cgi
sys.path.append("/home/protected/pkg")
sys.path.append("/home/sterna/Verkefni/Hellvar webpage/protected/pkg")

from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from markdown import markdown

from wsgi_app import db
import models

URLARG = "news.urlargs"

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

# handy helper functions
def render(template, *args, **kwargs):
    template = jinja_env.get_template(template)
    return [str(template.render(*args, **kwargs)), ]
    

def index(environ, start_response):
    posts = db.get(items=['id', 'title', 'text_body', 'published'],
                   where_not={'published': 'None'})
    
    start_response('200 OK', [('Content-Type', 'text/html')])
    return render('index.html', **locals())

def post_permalink(environ, start_response):
    args = environ[URLARG]
    post_id = args[0]
    post = db.fetch(items=['title', 'text_body', 'published'],
                    where={'id': post_id})

    if post['published'] is not None:
        start_response('200 OK', [('Content-Type', 'text/html')])
        return render('post.html', **locals())
    else:
        return not_found(environ, start_response)
