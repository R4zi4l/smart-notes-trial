from pathlib import Path
from configparser import ConfigParser

from tornado.web import Application, RequestHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import aiomysql

from .views import IndexHandler, ConnectionHandler


class RedirectHandler(RequestHandler):
    def get(self):
        self.redirect('https://' + self.request.host.split(':')[0] + self.request.uri, permanent=False)


class ClientsPool(list):
    def __init__(self, *args):
        super(ClientsPool, self).__init__(*args)


async def run(**kwargs):
    handlers = [
        (r'/connection', ConnectionHandler, {}, 'connection'),
        (r'.*', IndexHandler, {}, 'index'),
    ]

    folder = Path(__file__).parent

    config = ConfigParser()
    config.read(folder / 'settings.ini')

    settings = dict(
        static_path=folder / config.get('server', 'static_path', fallback='./static'),
        template_path=folder / config.get('server', 'template_path', fallback='./templates'),
        cookie_secret=config.get('server', 'cookie_secret', fallback='__CHANGE__THIS__WIERD__COOKIE_KEY_TO_SOMETHINF_IN_FUTURE__'),
        xsrf_cookies=True,
        debug=kwargs.get('debug', config.getboolean('debug', 'enabled', fallback=False)),
        static_url_prefix='/static/',
    )

    application = Application(handlers, **settings)

    try:
        application.database = await aiomysql.create_pool(
            host=config.get('database', 'host', fallback='127.0.0.1'),
            port=config.getint('database', 'port', fallback=3306),
            user=config.get('database', 'user', fallback='root'),
            password=config.get('database', 'password', fallback=''),
            db=config.get('database', 'database', fallback='db'),
            pool_recycle=20 # Bug fix: otherwise connection provides outdated content
        )
    
    except Exception as e:
        print('ERROR', 'run', 'failed to create connection pool to database', e, sep=' : ')
        IOLoop.instance().stop()
    

    application.clients = ClientsPool()

    certfile = config.get('ssl', 'certfile', fallback=None)
    keyfile = config.get('ssl', 'keyfile', fallback=None)

    options = dict(
        ssl_options={
            'certfile': certfile,
            'keyfile': keyfile,
        } if certfile and keyfile else None
    )

    if not settings['debug'] and certfile and keyfile:
        https_server = HTTPServer(application, **options)
        https_server.listen(443)

        redirect_application = Application([
            (r'.*', RedirectHandler),
        ])
        http_server = HTTPServer(redirect_application)
        http_server.listen(80)

    else:
        http_server = HTTPServer(application, **options)
        http_server.listen(config.get('debug', 'port', fallback=80))
