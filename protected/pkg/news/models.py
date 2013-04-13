import sys
sys.path.append('/home/sterna/Verkefni/Hellvar webpage/protected/pkg')
sys.path.append('/home/protected/pkg')

from wsgi_app import db

class News(db.Model):

    id = "INTEGER PRIMARY KEY"
    title = "TEXT UNIQUE"
    text_body = "TEXT"
    published = "TEXT"
    last_modified = "TEXT"
