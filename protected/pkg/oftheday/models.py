import sys
sys.path.append('/home/sterna/Verkefni/Hellvar webpage/protected/pkg')
sys.path.append('/home/protected/pkg')

from wsgi_app import db

class OfTheDay(db.Model):
    id = "INTEGER PRIMARY KEY"
    message = "TEXT"
