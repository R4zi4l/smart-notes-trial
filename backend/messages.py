from datetime import datetime, timedelta
from argon2 import PasswordHasher, exceptions
from uuid import uuid4
from functools import wraps


def required_auth(flag):
  def decorator(method):
    @wraps(method)
    async def wrapper(handler, *args, **kwargs):
      if bool(handler.current_user) == flag:
        return await method(handler, *args, **kwargs)
      else:
        return (False, {
          'status': 'error',
          'message': 'user have to be authorised' if flag else 'user already authorised',
        })
    return wrapper
  return decorator


async def message_status(handler, message): 
  try:
    session_id = handler.get_secure_cookie('session', message.get('session'), max_age_days=7)

    if session_id is None:
      handler.current_user = None
      return (False, {
        'status': 'ok',
        'session': None,
        'username': None,
      })
    
    session_id = session_id.decode('utf-8')
    
    async with handler.database.acquire() as connection:
      async with connection.cursor() as cursor:
        await cursor.execute('SELECT `owner`, `expired` FROM `session` WHERE `id` = %s', (session_id, ))

        if not cursor.rowcount:
          handler.current_user = None
          return (False, {
            'status': 'ok',
            'session': None,
            'username': None,
          })

        (owner, expired) = await cursor.fetchone()

        if expired <= datetime.now():
          handler.current_user = None
          return (False, {
            'status': 'ok',
            'session': None,
            'username': None,
          })

        if expired - timedelta(days=1) < datetime.now():
          await cursor.execute('UPDATE SET `expired` = %s, `updated` = %s WHERE `id` = %s',
            (expired + timedelta(days=7), datetime.now(), session_id))
          await connection.commit()

        await cursor.execute('SELECT `id`, `username` from `user` WHERE `id` = %s', (owner,))

        if not cursor.rowcount:
          handler.current_user = None
          return (False, {
            'status': 'ok',
            'session': None,
            'username': None,
          })

        (owner, username) = await cursor.fetchone()
        
        handler.current_user = owner
        return (False, {
          'status': 'ok',
          'session': handler.create_signed_value('session', session_id).decode('utf-8'),
          'username': username,
        })

  except Exception as e:
    print('ERROR', 'message_status', 'failed to get status', e, sep=' : ')
    return (False, {
      'status': 'error', 
      'message': 'failed to get status'
    })


@required_auth(False)
async def message_register(handler, message):
  hasher = PasswordHasher(hash_len=64, salt_len=64)

  async with handler.database.acquire() as connection:
    async with connection.cursor() as cursor:
      try:
        email = message.get('email')
        assert email

        await cursor.execute('SELECT `id` FROM `user` WHERE `email` = %s', (email,))
        assert not cursor.rowcount

      except:
        return (False, {
          'status': 'error',
          'type': 'email',
          'message': 'Invalid email or the user with such email already exists'
        })

      await cursor.execute('INSERT INTO `user` (`id`, `updated`, `email`, `username`, `password`) VALUE (%s, %s, %s, %s, %s)',
        (str(uuid4()), datetime.now(), message.get('email'), message.get('username'), hasher.hash(str(message.get('password')))))
      await connection.commit()
      
      return await message_login(handler, message)


@required_auth(False)
async def message_login(handler, message):
  hasher = PasswordHasher(hash_len=64, salt_len=64)

  async with handler.database.acquire() as connection:
    async with connection.cursor() as cursor:
      try:
        await cursor.execute('SELECT `id`, `username`, `password` FROM `user` WHERE `email` = %s', (message.get('email'),))
        assert cursor.rowcount

        (user, username, password) = await cursor.fetchone()

      except:
        return (False, {
          'status': 'error',
          'type': 'email',
          'message': 'Invalid email'
        })

      try:
        hasher.verify(password, message.get('password'))
      except exceptions.Argon2Error:
        return (False, {
          'status': 'error',
          'type': 'email',
          'message': 'Invalid password'
        })

      session = str(uuid4())
      await cursor.execute('INSERT INTO `session` (`id`, `owner`, `updated`, `started`, `expired`) VALUE (%s, %s, %s, %s, %s)',
        (session, user, datetime.now(), datetime.now(), datetime.now() + timedelta(days=7)))
      await connection.commit()
      
      handler.current_user = user
      return (False, {
        'status': 'ok',
        'session': handler.create_signed_value('session', session).decode('utf-8'),
        'username': username,
      })


@required_auth(True)
async def message_load_models(handler, message):
  async with handler.database.acquire() as connection:
    async with connection.cursor() as cursor:
      await cursor.execute('SELECT `id`, `updated`, `title`, `text` FROM `note` WHERE `owner` = %s', (handler.current_user,))
      note = { row[0] : row for row in await cursor.fetchall()}

      await cursor.execute('SELECT `id`, `updated`, `title`, `text`, `parent` FROM `category` WHERE `owner` = %s', (handler.current_user,))
      category = { row[0] : row for row in await cursor.fetchall()}

      await cursor.execute('SELECT `category`, `entity`, `updated` FROM `categoryentity` WHERE `owner` = %s', (handler.current_user,))
      categoryentity = { row[0] + row[1] : row for row in await cursor.fetchall()}
  
  return (False, {
    'status': 'ok',
    'note': note,
    'category': category,
    'categoryentity': categoryentity,
  })


@required_auth(True)
async def message_update_models_items(handler, message):
  accepted = []
  rejected = []

  for item in message['items']:
    try:
      status = item['status']
      model = item['model']
      key = item['id']
      values = [(key, value) for key, value in item['item'].items()]
      updated = datetime.strptime(item['updated'], '%Y-%m-%d %H:%M:%S.%f')
    
      await globals()['process_' + model + '_model_update'](handler, updated, status, key, values)

    except Exception as e:
      item['error'] = str(e)
      rejected.append(item)
    
    else:
      accepted.append(item)

  return (True, {
    'status': 'ok',
    'id': message['id'],
    'type': 'update_models_items',
    'accepted': accepted,
    'rejected': rejected,
  })


async def process_note_model_update(handler, updated, status, key, values):
  owner = handler.current_user

  values = [item for item in values if item[0] != 'id']

  async with handler.database.acquire() as connection:
    async with connection.cursor() as cursor:
      await cursor.execute('SELECT `updated` FROM `note` WHERE `owner`=%s AND `id`=%s', (owner, key))
      assert status == 'insert' or updated == (await cursor.fetchone())[0], f"outdated data version: {key}, {updated}"

      if status == 'insert':
        query = 'INSERT INTO `note` ({}) VALUES({})'.format(
          ','.join(['`owner`', '`id`'] + [f'`{value[0]}`' for value in values]),
          ','.join(['%s'] * (2 + len(values)))
        )
        args = (owner, key) + tuple(value[1] for value in values)
      elif status == 'update':
        query = 'UPDATE `note` SET {} WHERE `owner`=%s AND `id`=%s'.format(
          ','.join([f'{value[0]} = %s' for value in values])
        )
        args = tuple(value[1] for value in values) + (owner, key)
      elif status == 'delete':
        query = 'DELETE FROM `note` WHERE `owner`=%s AND `id`=%s'
        args = (owner, key)
      else:
        raise Exception('invalid model item status:', status)
      
      await cursor.execute(query, args)
      await connection.commit()
  

async def process_category_model_update(handler, updated, status, key, values):
  owner = handler.current_user
  
  values = [item for item in values if item[0] != 'id']

  async with handler.database.acquire() as connection:
    async with connection.cursor() as cursor:    
      await cursor.execute('SELECT `updated` FROM `category` WHERE `owner`=%s AND `id`=%s', (owner, key))
      assert status == 'insert' or updated == (await cursor.fetchone())[0], f"outdated data version: {key}, {updated}"

      if status == 'insert':
        query = 'INSERT INTO `category` ({}) VALUES({})'.format(
          ','.join(['`owner`', '`id`'] + [f'`{value[0]}`' for value in values]),
          ','.join(['%s'] * (2 + len(values)))
        )
        args = (owner, key) + tuple(value[1] for value in values)
      elif status == 'update':
        query = 'UPDATE `category` SET {} WHERE `owner`=%s AND `id`=%s'.format(
          ','.join([f'{value[0]} = %s' for value in values])
        )
        args = tuple(value[1] for value in values) + (owner, key)
      elif status == 'delete':
        query = 'DELETE FROM `category` WHERE `owner`=%s AND `id`=%s'
        args = (owner, key)
      else:
        raise Exception('invalid model item status:', status)
      
      await cursor.execute(query, args)
      await connection.commit()


async def process_categoryentity_model_update(handler, updated, status, key, values):
  owner = handler.current_user
  category = key[:36]
  entity = key[36:]

  values = [item for item in values if item[0] != 'category' and item[0] != 'entity']

  async with handler.database.acquire() as connection:
    async with connection.cursor() as cursor:
      await cursor.execute('SELECT `updated` FROM `categoryentity` WHERE `owner`=%s AND `category`=%s AND `entity`=%s', (owner, category, entity))
      assert status == 'insert' or updated == (await cursor.fetchone())[0], f"outdated data version: {key}, {updated}"

      if status == 'insert':
        query = 'INSERT INTO `categoryentity` ({}) VALUES({})'.format(
          ','.join(['`owner`', '`category`', '`entity`'] + [f'`{value[0]}`' for value in values]),
          ','.join(['%s'] * (3 + len(values)))
        )
        args = (owner, category, entity) + tuple(value[1] for value in values)
      elif status == 'update':
        query = 'UPDATE `categoryentity` SET {} WHERE `owner`=%s AND `category`=%s AND `entity`=%s'.format(
          ','.join([f'{value[0]} = %s' for value in values])
        )
        args = tuple(value[1] for value in values) + (owner, category, entity)
      elif status == 'delete':
        query = 'DELETE FROM `categoryentity` WHERE `owner`=%s AND `category`=%s AND `entity`=%s'
        args = (owner, category, entity)
      else:
        raise Exception('invalid model item status:', status)

      await cursor.execute(query, args)
      await connection.commit()
