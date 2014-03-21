import os, sys

sys.path.insert(0, '/oversight/config')
sys.path.insert(0, '/oversight/code')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from cherrypy import wsgiserver
from oversight.wsgi import application

d = wsgiserver.WSGIPathInfoDispatcher({'/': application})
server = wsgiserver.CherryPyWSGIServer(('127.0.0.1', 8080), d)

if __name__ == '__main__':
   try:
      server.start()
   except KeyboardInterrupt:
      server.stop()
