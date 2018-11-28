import os, sys

sys.path.insert(0, './config')
sys.path.insert(0, '.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from cheroot.wsgi import Server as wsgiserver
from cheroot.wsgi import WSGIPathInfoDispatcher
from oversight.wsgi import application

d = WSGIPathInfoDispatcher({'/': application})
server = wsgiserver(('127.0.0.1', 8080), d)

if __name__ == '__main__':
   try:
      server.start()
   except KeyboardInterrupt:
      server.stop()
