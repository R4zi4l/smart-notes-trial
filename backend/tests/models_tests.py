from tornado.ioloop import IOLoop
from tornado.testing import gen_test, AsyncTestCase

import asyncio
import aiomysql

from datetime import datetime

from ..models import User


class TestUser(AsyncTestCase):
    connection = None

    def get_new_ioloop(self):
        return IOLoop.current()

    @classmethod
    def setUpClass(cls):
        cls.connection = asyncio.get_event_loop().run_until_complete(
            aiomysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='root',
                db='smartnotestest'
            )
        )

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    @gen_test
    async def test_select(self):
        async with self.connection.cursor() as cursor:
            await cursor.execute('DELETE FROM `owner`')
            await cursor.execute('INSERT INTO `user` (`id`, `email`, `username`, `password`, `updated`) VALUE("b2f0683c-cc42-11ea-93df-0a0027000007", "first email", "first username", "first password", NOW());')
            
        users = await User.select(self.connection, id='b2f0683c-cc42-11ea-93df-0a0027000007')
        
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, 'b2f0683c-cc42-11ea-93df-0a0027000007')
        self.assertEqual(users[0].email, 'first email')

    @gen_test
    async def test_save_user(self):
        async with self.connection.cursor() as cursor:
            await cursor.execute('DELETE FROM `owner`')
        
        users = await User.select(self.connection, id='b2f0683c-cc42-11ea-93df-0a0027000007')
        self.assertEqual(len(users), 0)

        user = User(id='b2f0683c-cc42-11ea-93df-0a0027000007', email='first@first.com', username='firstusername', password='verystrongfirstpassword')
        await user.save(self.connection, datetime.now())
        
        users = await User.select(self.connection, id='b2f0683c-cc42-11ea-93df-0a0027000007')
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, 'firstusername')

        user.username = 'FIRSTusername'
        await user.save(self.connection, datetime.now())

        users = await User.select(self.connection, id='b2f0683c-cc42-11ea-93df-0a0027000007')
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, 'FIRSTusername')
        