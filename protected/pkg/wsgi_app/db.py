# wsgi_app/db.py
# ==========
# A parent module to handle repeted database actions

import sqlite3 as sql
# TODO on publicity, change absolute path "/home/protected/database.db"
database = "/home/sterna/Verkefni/Hellvar webpage/protected/database.db"


def _get(func, items, where=None, where_not=None):
    """
    select a sql row object from the database and return them
    by the given function
    """
    
    conn = sql.connect(database)
    conn.row_factory = sql.Row
    with conn:
        cur = conn.cursor()

        if where is not None:
            select_query = """
                SELECT {0} FROM News WHERE {1} = ?
            """.format(', '.join(items), where.keys()[0])
            cur.execute(select_query, where.values())
        elif where_not is not None:
            select_query = """
                SELECT {0} FROM News WHERE {1} != ?
            """.format(', '.join(items), where_not.keys()[0])
            cur.execute(select_query, where_not.values())
        else:
            select_query = """
                SELECT {0} FROM News
            """.format(', '.join(items))
            cur.execute(select_query)

        callback = getattr(cur, func)
        return callback()

def get(items, where=None, where_not=None):
    "select a sql row object from the database and return a list of them all"
    return list(_get('fetchall', items, where, where_not))
        
def fetch(items, where=None, where_not=None):
    "select a sql row object from the database and return the first"
    return _get('fetchone', items, where, where_not)
        
class Transaction(object):
    
    def __init__(self):
        self.conn = sql.connect(database)
    
    def insert(self, **kwargs):
        """
        Makes an INSERT query into the 'News' table of the database.
        insert(title='my_title', post='A new News post about me') will
        create the SQL query: "INSERT INTO News (title, post)
        VALUES ('my_title', 'A new News post about me')"
        """
        cur = self.conn.cursor()
        insert_query = """
            INSERT INTO News ({0}) VALUES ({1})
        """.format(', '.join(kwargs.keys()),
                   ', '.join([':' + key for key in kwargs.keys()]))

        cur.execute(insert_query, kwargs)
        
    def update(self, where='', **kwargs):
        cur = self.conn.cursor()
        update_query = """
            UPDATE News
            SET {0}
            WHERE {1} = {2}
        """.format(', '.join([key+' = :'+key for key in kwargs.keys()]),
                   where.keys()[0], ':' + where.keys()[0])
        if where:
            kwargs[where.keys()[0]] = where.values()[0]
        cur.execute(update_query, kwargs)
        
    def delete(self, where=''):
        cur = self.conn.cursor()
        delete_query = """
            DELETE FROM News
            WHERE {0} = {1}
        """.format(where.keys()[0], ':' + where.keys()[0])
        
        cur.execute(delete_query, where)
    
    def save(self):
        self.conn.commit()
        
    def __del__(self):
        self.conn.close()
