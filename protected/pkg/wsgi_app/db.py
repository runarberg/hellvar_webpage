# wsgi_app/db.py
# ==========
# A parent module to handle repeted database actions

import sqlite3 as sql
# TODO on publicity, change absolute path "/home/protected/database.db"
database = "/home/sterna/Verkefni/Hellvar webpage/protected/database.db"

class Model(object):
    """
    A parent model to handle all database transaction
    """

    def __init__(self):
        self.conn = sql.connect(database, check_same_thread=False)
        self.conn.row_factory = sql.Row
        self.name = self.__class__.__name__

        
    def _get(self, func, items, where=None, where_not=None):
        """
        select a sql row object from the database and return them
        by the given function
        """
                
        cur = self.conn.cursor()
            
        format_args = {'items': ', '.join(items),
                       'table': self.name}
            
        if where is not None:
            format_args['key'] = where.keys()[0]

            select_query = """
            SELECT {items} FROM {table} WHERE {key} = ?
            """.format(**format_args)
            
            cur.execute(select_query, where.values())
            
        elif where_not is not None:
            format_args['key'] = where_not.keys()[0]
            
            select_query = """
            SELECT {items} FROM {table} WHERE {key} != ?
            """.format(**format_args)
            
            cur.execute(select_query, where_not.values())
            
        else:
            select_query = """
            SELECT {items} FROM {table}
            """.format(**format_args)
            
            cur.execute(select_query)
            
        callback = getattr(cur, func)
        return callback()
            
    def get(self, items, where=None, where_not=None):
        "select a sql row object from the database and return a list of them all"
        items = self._get('fetchall', items, where, where_not)
        if items:
            return list(items)
        
    def fetch(self, items, where=None, where_not=None):
        "select a sql row object from the database and return the first"
        return self._get('fetchone', items, where, where_not)
        

    def reset(self):
        cur = self.conn.cursor()
        fields = [' '.join((attr, getattr(self, attr)))
                  for attr in dir(self)
                  if isinstance(attr, str) and not attr.startswith('__')]
        format_args = {'name': self.name,
                       'field_str': ', '.join(fields)}
        
        create_query = """
            CREATE TABLE {name} ({field_str})
        """.format(**format_args)

        cur.execute("DROP TABLE IF EXISTS {0}".format(self.name))
        cur.execute(create_query)

    def insert(self, items=''):
        """
        Makes an INSERT query into the 'News' table of the database.
        insert(items={'title': 'my_title', 'post': 'A new News post 
        about me'}) will create the SQL query: "INSERT INTO News 
        (title, post) VALUES ('my_title', 'A new News post about me')"
        """
        cur = self.conn.cursor()

        format_args = {'table': self.name,
                       'items': ', '.join(items.keys()),
                       'values': ', '.join([':'+key for key in items.keys()])}
        
        insert_query = """
            INSERT INTO {table} ({items}) VALUES ({values})
        """.format(**format_args)

        cur.execute(insert_query, items)
        
    def update(self, items=None, where=None):
        cur = self.conn.cursor()

        format_args = {'table': self.name,
                       'item_value_pairs':
                           ', '.join([key+' = :'+key for key in items.keys()]),
                       'where_key': where.keys()[0]}
        
        update_query = """
            UPDATE {table}
            SET {item_value_pairs}
            WHERE {where_key} = :{where_key}
        """.format(**format_args)

        sql_args = dict(where.items() + items.items())
        
        cur.execute(update_query, sql_args)
        
    def delete(self, where=None):
        cur = self.conn.cursor()
        delete_query = """
            DELETE FROM {table}
            WHERE {key} = :{key}
        """.format(table=self.name, key=where.keys()[0])
        
        cur.execute(delete_query, where)
    
    def save(self):
        self.conn.commit()
        
    def __del__(self):
        self.conn.close()
