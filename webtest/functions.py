
def application(environ, start_response):
    """docstring for application"""
    body = b'<html>'
    headers = [('Content-Type', 'text/html; charset=utf8'),
               ('Content-Length', str(len(body)))]
    start_response('200 OK', headers)
    return [body]
