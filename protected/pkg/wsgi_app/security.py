# -*- coding: utf-8 -*-

from collections import namedtuple
import hashlib

class User(namedtuple('User', ['username', 'password'])):
    __slots__ = ()
    def __str__(self):
        return str(self.username)
        
USERS = [User(username='<username>', password='<password>')]
SECRET_HASH = "<string>"


def make_hash(str):
    return hashlib.md5(str + SECRET_HASH).hexdigest()

def make_secure_val(str):
    return '||'.join((str, make_hash(str)))

def check_secure_val(str):
    if "|" in str:
        val, hash = str.split('||')
        if make_hash(val) == hash:
            return val

