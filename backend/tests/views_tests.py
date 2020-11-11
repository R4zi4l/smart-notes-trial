import json
import time

from unittest.mock import patch
from datetime import datetime, timedelta
from argon2 import PasswordHasher, exceptions

from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.httputil import HTTPHeaders
from tornado.httpclient import HTTPRequest
from tornado.web import create_signed_value
from tornado.websocket import websocket_connect
from tornado import gen

from argon2 import PasswordHasher, exceptions

from ..app import Application
from ..models import Session, User
from ..views import ConnectionHandler


class TestIndexHandler(AsyncHTTPTestCase):
    def get_app(self):
        return Application(debug=False)

    @patch('backend.models.Session.save')
    @patch('backend.models.Session.objects')
    def test_prepare_session_cookie_not_set_or_invalid(self, objects, save):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)

        headers = HTTPHeaders({'content-type': 'text/html'})
        headers.add('Set-Cookie', 'session=1')
        response = self.fetch('/', headers=headers)
        self.assertEqual(response.code, 200)

        headers = HTTPHeaders({'content-type': 'text/html'})
        headers.add('Set-Cookie', 'session')
        response = self.fetch('/', headers=headers)
        self.assertEqual(response.code, 200)

        headers = HTTPHeaders({'content-type': 'text/html'})
        headers.add('Set-Cookie', 'session=aj;flam;lkaf')
        response = self.fetch('/', headers=headers)
        self.assertEqual(response.code, 200)

        objects.assert_not_called()
        save.assert_not_called()

    @patch('backend.models.Session.save')
    @patch('backend.models.Session.objects')
    def test_prepare_session_not_found(self, objects, save):
        def session_objects(id):
            return []
        objects.side_effect = session_objects

        headers = HTTPHeaders({'content-type': 'text/html'})
        headers.add('Cookie', 'session=' + create_signed_value(self._app.settings["cookie_secret"], 'session', (1).to_bytes(10, byteorder='big')).decode('utf-8'))
        response = self.fetch('/', headers=headers)
        self.assertEqual(response.code, 200)
        objects.assert_called_with(id=1)

        headers = HTTPHeaders({'content-type': 'text/html'})
        headers.add('Cookie', 'session=' + create_signed_value(self._app.settings["cookie_secret"], 'session', (112222548938).to_bytes(10, byteorder='big')).decode('utf-8'))
        response = self.fetch('/', headers=headers)
        self.assertEqual(response.code, 200)
        objects.assert_called_with(id=112222548938)

        save.assert_not_called()

    @patch('backend.models.Session.save')
    @patch('backend.models.Session.objects')
    def test_prepare_session_expired(self, objects, save):
        def session_objects(id):
            return [Session(id=id, expired=datetime.now() - timedelta(hours=10), user=1)]
        objects.side_effect = session_objects

        headers = HTTPHeaders({'content-type': 'text/html'})
        headers.add('Cookie', 'session=' + create_signed_value(self._app.settings["cookie_secret"], 'session', (1).to_bytes(10, byteorder='big')).decode('utf-8'))
        response = self.fetch('/', headers=headers)
        self.assertEqual(response.code, 200)
        objects.assert_called_with(id=1)
        save.assert_not_called()

    @patch('backend.models.Session.save')
    @patch('backend.models.Session.objects')
    def test_prepare_session_new(self, objects, save):
        def session_objects(id):
            return [Session(id=id, expired=datetime.now() + timedelta(hours=18), user=1)]
        objects.side_effect = session_objects

        headers = HTTPHeaders({'content-type': 'text/html'})
        headers.add('Cookie', 'session=' + create_signed_value(self._app.settings["cookie_secret"], 'session', (1).to_bytes(10, byteorder='big')).decode('utf-8'))
        response = self.fetch('/', headers=headers)
        self.assertEqual(response.code, 200)
        objects.assert_called_with(id=1)
        save.assert_not_called()

    @patch('backend.models.Session.save')
    @patch('backend.models.Session.objects')
    def test_prepare_session_old(self, objects, save):
        def session_objects(id):
            return [Session(id=id, expired=datetime.now() + timedelta(hours=6), user=1)]
        objects.side_effect = session_objects

        headers = HTTPHeaders({'content-type': 'text/html'})
        headers.add('Cookie', 'session=' + create_signed_value(self._app.settings["cookie_secret"], 'session', (1).to_bytes(10, byteorder='big')).decode('utf-8'))
        response = self.fetch('/', headers=headers)
        self.assertEqual(response.code, 200)
        objects.assert_called_with(id=1)
        save.assert_called_once()


class TestConnectionHandler(AsyncHTTPTestCase):
    def get_app(self):
        return Application(debug=False)

    @patch('backend.views.ConnectionHandler.message_status')
    @gen_test
    async def test_on_message(self, message_status):
        def test(data):
            return ('test', data)
        message_status.side_effect = test

        url = "ws://localhost:" + str(self.get_http_port()) + "/connection"
        client = await websocket_connect(url)

        # websocket message has wrong structure
        message = json.dumps('akuna matata')
        client.write_message(message)
        response = json.loads(await client.read_message())
        self.assertEqual(response.get('type'), 'error')

        # websocket message has wrong type
        message = json.dumps({
            'type': '123',
            'data': None,
        })
        client.write_message(message)
        response = json.loads(await client.read_message())
        self.assertEqual(response.get('type'), 'error')

        # websocket message has correct type
        message = json.dumps({
            'type': 'status',
            'data': { 'example': 123 },
        })
        client.write_message(message)
        response = json.loads(await client.read_message())
        self.assertEqual(response.get('type'), 'test')
        message_status.assert_called_with({ 'example': 123 })

    @patch('backend.models.Session.objects')
    @patch('backend.models.User.objects')
    @gen_test
    async def test_message_status_without_session(self, user_obects, session_objects):
        user_obects.return_value = []
        session_objects.return_value = []

        client = await websocket_connect(HTTPRequest(
            "ws://localhost:" + str(self.get_http_port()) + "/connection",
        ))

        client.write_message(json.dumps({
            'type': 'status',
            'data': None,
        }))
        response = json.loads(await client.read_message())
        self.assertEqual(response.get('type'), 'status')
        self.assertEqual(response.get('data'), {
            'user': None,
            'username': None,
        })
        user_obects.assert_called_once()
        session_objects.assert_not_called()

    @patch('backend.models.Session.objects')
    @patch('backend.models.User.objects')
    @gen_test
    async def test_message_status_with_session(self, user_objects, session_objects):
        user_objects.return_value = [User(
            id=12,
            username='Pavel',
            password='Teftelev'
        )]
        session_objects.return_value = [Session(
            id=1,
            expired=datetime.now() + timedelta(hours=24),
            user=12
        )]

        headers = HTTPHeaders({'content-type': 'text/html'})
        headers.add('Cookie', 'session=' + create_signed_value(self._app.settings.get("cookie_secret"), 'session', (1).to_bytes(10, byteorder='big'), clock=time.time).decode('utf-8'))
        client = await websocket_connect(HTTPRequest(
            "ws://localhost:" + str(self.get_http_port()) + "/connection",
            headers=headers,
        ))

        client.write_message(json.dumps({
            'type': 'status',
            'data': None,
        }))
        response = json.loads(await client.read_message())
        self.assertEqual(response.get('type'), 'status')
        self.assertEqual(response.get('data'), {
            'user': 12,
            'username': 'Pavel',
        })
        user_objects.assert_called_once()
        session_objects.assert_called_once()

    @gen_test
    async def test_decorator_authorisation_needed(self):
        class Test:
            def __init__(self):
                self.current_user = None

            @ConnectionHandler.authorisation_needed(True)
            async def auth_true(self, data):
                return data

            @ConnectionHandler.authorisation_needed(False)
            async def auth_false(self, data):
                return data
        test = Test()

        result = await test.auth_true('this is test data string')
        self.assertEqual(result, ('error', {
            'message': 'user have to be authorised',
        }))

        result = await test.auth_false('this is test data string')
        self.assertEqual(result, 'this is test data string')

        test.current_user = 1

        result = await test.auth_true('this is test data string')
        self.assertEqual(result, 'this is test data string')

        result = await test.auth_false('this is test data string')
        self.assertEqual(result, ('error', {
            'message': 'user already authorised',
        }))

    async def setup_websocket_connection(self, session_id=None):
        if session_id:
            headers = HTTPHeaders({'content-type': 'text/html'})
            headers.add('Cookie', 'session=' + create_signed_value(self._app.settings.get("cookie_secret"), 'session', (session_id).to_bytes(10, byteorder='big'), clock=time.time).decode('utf-8'))
            return (await websocket_connect(HTTPRequest(
                "ws://localhost:" + str(self.get_http_port()) + "/connection",
                headers=headers,
            )))
        else:
            return (await websocket_connect(HTTPRequest(
                "ws://localhost:" + str(self.get_http_port()) + "/connection",
            )))

    def setup_auth_environment(self, model_save, model_objects, session_objects, user_objects, create_session):
        session_objects.return_value = [Session(
            id=1,
            expired=datetime.now() + timedelta(hours=24),
            user=12,
        )]
        create_session.return_value = Session(
            id=1,
            expired=datetime.now() + timedelta(hours=24),
            user=12,
        )
        hasher = PasswordHasher(hash_len=64, salt_len=64)
        user_objects.return_value = [User(
            id=12,
            username='789',
            password=hasher.hash('789'),
        )]

    @patch('backend.views.ConnectionHandler.create_session')
    @patch('backend.models.User.objects')
    @patch('backend.models.Session.objects')
    @patch('backend.database.Model.objects')
    @patch('backend.database.Model.save')
    @gen_test
    async def test_message_login_passed(self, model_save, model_objects, session_objects, user_objects, create_session):
        self.setup_auth_environment(model_save, model_objects, session_objects, user_objects, create_session)

        client = await self.setup_websocket_connection()
        client.write_message(json.dumps({
            'type': 'login',
            'data': {
                'username': '789',
                'password': '789',
            },
        }))

        response = json.loads(await client.read_message())
        self.assertEqual(response.get('type'), 'auth')
        self.assertEqual(response.get('data').get('user'), 12)
        model_save.assert_not_called()
        session_objects.assert_not_called()
        user_objects.assert_called_once()
        create_session.assert_called_once()

    @patch('backend.views.ConnectionHandler.create_session')
    @patch('backend.models.User.objects')
    @patch('backend.models.Session.objects')
    @patch('backend.database.Model.objects')
    @patch('backend.database.Model.save')
    @gen_test
    async def test_message_login_wrong_password(self, model_save, model_objects, session_objects, user_objects, create_session):
        self.setup_auth_environment(model_save, model_objects, session_objects, user_objects, create_session)

        client = await self.setup_websocket_connection()
        client.write_message(json.dumps({
            'type': 'login',
            'data': {
                'username': '789',
                'password': '78888',
            },
        }))

        response = json.loads(await client.read_message())
        self.assertEqual(response.get('type'), 'error')
        self.assertEqual(response.get('data').get('message'), 'Invalid password')
        model_save.assert_not_called()
        session_objects.assert_not_called()
        user_objects.assert_called_once()
        create_session.assert_not_called()

    @patch('backend.views.ConnectionHandler.create_session')
    @patch('backend.models.User.objects')
    @patch('backend.models.Session.objects')
    @patch('backend.database.Model.objects')
    @patch('backend.database.Model.save')
    @gen_test
    async def test_message_login_user_already_logged(self, model_save, model_objects, session_objects, user_objects, create_session):
        self.setup_auth_environment(model_save, model_objects, session_objects, user_objects, create_session)

        client = await self.setup_websocket_connection(1)
        client.write_message(json.dumps({
            'type': 'login',
            'data': {
                'username': '789213',
                'password': '789',
            },
        }))

        response = json.loads(await client.read_message())
        self.assertEqual(response.get('type'), 'error')
        self.assertEqual(response.get('data').get('message'), 'user already authorised')
        model_save.assert_not_called()
        session_objects.assert_called_once()
        user_objects.assert_not_called()
        create_session.assert_not_called()

    @patch('backend.views.ConnectionHandler.create_session')
    @patch('backend.models.User.objects')
    @patch('backend.models.Session.objects')
    @patch('backend.database.Model.objects')
    @patch('backend.database.Model.save')
    @gen_test
    async def test_message_reigster_passed(self, model_save, model_objects, session_objects, user_objects, create_session):
        self.setup_auth_environment(model_save, model_objects, session_objects, user_objects, create_session)
        user_objects.return_value = []

        client = await self.setup_websocket_connection()
        client.write_message(json.dumps({
            'type': 'register',
            'data': {
                'username': '789',
                'password': '789',
            },
        }))

        response = json.loads(await client.read_message())
        self.assertEqual(response.get('type'), 'auth')
        self.assertEqual(response.get('data').get('username'), '789')
        model_save.assert_called_once()
        model_objects.assert_not_called()
        session_objects.assert_not_called()
        user_objects.assert_called_once()
        create_session.assert_called_once()

    @patch('backend.views.ConnectionHandler.create_session')
    @patch('backend.models.User.objects')
    @patch('backend.models.Session.objects')
    @patch('backend.database.Model.objects')
    @patch('backend.database.Model.save')
    @gen_test
    async def test_message_logout_passed(self, model_save, model_objects, session_objects, user_objects, create_session):
        self.setup_auth_environment(model_save, model_objects, session_objects, user_objects, create_session)
        user_objects.return_value = []

        client = await self.setup_websocket_connection(1)
        client.write_message(json.dumps({
            'type': 'logout',
            'data': {
                'username': '789',
                'password': '789',
            },
        }))

        response = json.loads(await client.read_message())
        self.assertEqual(response.get('type'), 'auth')
        self.assertEqual(response.get('data').get('username'), None)
        model_save.assert_not_called()
        model_objects.assert_not_called()
        session_objects.assert_called_once()
        user_objects.assert_not_called()
        create_session.assert_not_called()
