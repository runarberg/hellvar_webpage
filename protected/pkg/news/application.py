import re
import views, urls

def not_found(environ, start_response):
    start_response("404 NOT FOUND", [("Content-Type", "text/plain")])
    return ["Not found", ]

def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, callback in urls.URLS:
        match = re.search(regex, path)
        if match is not None:
            environ[views.URLARG] = match.groups()
            return callback(environ, start_response)
    return not_found(environ, start_response)
