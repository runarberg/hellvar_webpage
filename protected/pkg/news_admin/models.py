from datetime import datetime

import db

# TODO on publicity, REMOVE sql support from this module
import sqlite3 as sql
database = "/home/sterna/Verkefni/Hellvar webpage/protected/database.db"

def new_post(title, text_body, time=""):
    if not time:
        time = datetime.now()
    
    trans = db.Transaction()
    trans.insert(title=title, text_body=text_body, last_modified=time)
    trans.save()
    
def update_post(post_id, title, text_body, time=""):
    if not time:
        time = datetime.now()
    
    trans = db.Transaction()
    trans.update(title=title, text_body=text_body,
                 last_modified=time, where={'id': post_id})
    trans.save()

def publish_post(post_id):
    time = datetime.now()
    
    trans = db.Transaction()
    trans.update(published=time, where={'id': post_id})
    trans.save()
    
def unpublish_post(post_id):
    
    trans = db.Transaction()
    trans.update(published='', where={'id': post_id})
    trans.save()
    
def delete_posts(post_id):

    trans = db.Transaction()
    try:
        for id in post_id:
            trans.delete(where={'id': id})
    except TypeError:
        trans.delete(where={'id': post_id})
    trans.save()
    
    
# TODO REMOVE THIS FUNCTION BEFORE PUBLICITY
def reset_posts():
    conn = sql.connect(database)
    
    with conn:
        cur = conn.cursor()
        create_query = """
            CREATE TABLE News (id            INTEGER PRIMARY KEY,
                               title         TEXT UNIQUE,
                               text_body     TEXT,
                               published     TEXT,
                               last_modified TEXT)
        """
        
        cur.execute("DROP TABLE IF EXISTS News")
        cur.execute(create_query)
