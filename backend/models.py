from itertools import chain
from datetime import datetime, timedelta

import aiomysql


class Field:
    pass


class Model:
    fields = []
    select_query = ''

    @staticmethod
    def init(cls):
        cls.fields = []

        for name in dir(cls):
            value = getattr(cls, name)
            if isinstance(value, Field):
                cls.fields.append(name)
        
        cls.select_query = 'SELECT {} FROM `{}`'.format(
            ','.join([f'`{field}`' for field in cls.fields]),
            cls.__name__.lower()
        )
        return cls
    
    @classmethod
    async def select(cls, connection, **kwargs):
        async with connection.cursor() as cursor:
            where = []

            for key, value in kwargs.items():
                if key in cls.fields:
                    if type(value) in [list, tuple]:
                        where.append((key, ','.join(['%s']*len(value)), value))
                    else:
                        where.append((key, '%s', [value]))

            query = cls.select_query
            if len(where):
                query += ' WHERE ' + ' AND '.join([f'`{condition[0]}` IN ({condition[1]})' for condition in where])
                
            
            result = []
            if await cursor.execute(query, tuple(chain.from_iterable([item[2] for item in where]))):
                for row in await cursor.fetchall():
                    item = cls()
                    for idx, value in enumerate(cls.fields):
                        setattr(item, value, row[idx])
                    result.append(item)
            return result
    
    def __init__(self, **kwargs):
        for name in kwargs:
            if name in self.__class__.fields:
                setattr(self, name, kwargs.get(name))

    def __str__(self):
        return '{' + ','.join([f'"{name}":"{getattr(self, name)}"' for name in self.__class__.fields if not isinstance(getattr(self, name), Field)]) + '}'

    async def save(self, connection, updated):
        fields = []
        data = []
        values = []
        updates = []

        self.updated = updated

        for name in self.__class__.fields:
            value = getattr(self, name)
            if not isinstance(value, Field):
                fields.append(f'`{name}`')
                data.append(value)
                values.append('%s')
                updates.append(f'`{name}`=%s')
        
        async with connection.cursor() as cursor:
            query = 'INSERT INTO {} ({}) VALUE ({}) ON DUPLICATE KEY UPDATE {}'.format(
                self.__class__.__name__.lower(),
                ','.join(fields),
                ','.join(values),
                ','.join(updates)
            )
            args = data + data
            await cursor.execute(query, args)


@Model.init
class User(Model):
    id = Field()
    updated = Field()
    email = Field()
    username = Field()
    password = Field()

    @classmethod
    async def select_by_id(cls, connection, id):
        try:
            return (await cls.select(connection, id=id))[0]
        except:
            return None # ToDo: add error message
    
    @classmethod
    async def select_by_email(cls, connection, email):
        try:
            return (await cls.select(connection, email=email))[0]
        except:
            return None # ToDo: add error message


@Model.init
class Session(Model):
    id = Field()
    owner = Field()
    updated = Field()
    started = Field()
    expired = Field()

    @classmethod
    async def select_by_id(cls, connection, id):
        try:
            return (await cls.select(connection, id=id))[0]
        except:
            return None # ToDo: add error message
    
    async def extend(self, connection, days):
        self.expired = datetime.now() + timedelta(days=days)
        await self.save(connection, datetime.now())


@Model.init
class Event(Model):
    id = Field()
    owner = Field()
    updated = Field()
    text = Field()
    scheduled = Field()
    done = Field()
    income = Field()
    expense = Field()
    source = Field()


@Model.init
class Note(Model):
    id = Field()
    owner = Field()
    updated = Field()
    text = Field()
    title = Field()


@Model.init
class Board(Model):
    id = Field()
    owner = Field()
    updated = Field()
    title = Field()
    text = Field()


@Model.init
class Category(Model):
    id = Field()
    owner = Field()
    updated = Field()
    title = Field()
    text = Field()
    parent = Field()


@Model.init
class BoardNote(Model):
    owner = Field()
    board = Field()
    note = Field()
    updated = Field()


@Model.init
class CategoryEntity(Model):
    owner = Field()
    category = Field()
    entity = Field()
    updated = Field()
