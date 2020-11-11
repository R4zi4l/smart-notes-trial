from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

from datetime import date, time, datetime
import json
from asyncio import Lock

from . import messages


def json_converter(o):
    if isinstance(o, datetime) or isinstance(o, date) or isinstance(o, time):
        return str(o)


class IndexHandler(RequestHandler):
  async def get(self):
    self.render('desktop.html')


class ConnectionHandler(WebSocketHandler):
  def check_origin(self, origin):
    return True
  
  def initialize(self):
    self.clients = self.application.clients
    self.database = self.application.database

  def open(self):
    self.current_user = None
    self.lock = Lock()
    self.clients.append(self)

  def on_close(self):
     self.clients.remove(self)

  async def on_message(self, message):
    try:
      request = json.loads(message)

    except Exception as e: 
      print('ERROR', 'ConnectionHandler.on_message', 'failed to get data from message with json parser', e, sep=' : ')

    else:
      try:
        request_id = str(request['id'])
        request_type = str(request['type'])
        request_message = request['message']

      except Exception as e:
        print('ERROR', 'ConnectionHandler.on_message', 'failed to get message parameters', e, sep=' : ')

      else:
        try:
          if request_type == 'request':
            (broadcast, response) = await self.handle_messsage(request_message)

            try:
              self.write_message(
                json.dumps(
                  {
                    'id': request_id,
                    'type': 'response',
                    'message': response,
                  }, 
                  default=json_converter
                )
              )
            except Exception as e:
              print('ERROR', 'ConnectionHandler.on_message', 'can\'t convert response message to json format', request_id, request_type, response, e, sep=' : ')

          elif request_type == 'notify':
            (broadcast, response) = await self.handle_messsage(request_message)

          else:
            print('ERROR', 'ConnectionHandler.on_message', 'unnknown message type', request_type, sep=' : ')

          if broadcast:
            for client in self.clients:
              if client != self and client.current_user == self.current_user:
                client.write_message(
                  json.dumps(
                    {
                      'id': request_id,
                      'type': 'notify',
                      'message': response,
                    }, 
                    default=json_converter
                  )
                )

        except Exception as e:
          print('ERROR', 'ConnectionHandler.on_message', 'unnknown error occured on message', request_id, request_type, e, sep=' : ')
  
  async def handle_messsage(self, message):
    try:
      message_type = str(message['type'])
      message_handler = getattr(messages, 'message_' + message_type)
    
    except Exception as e:
      print('ERROR', 'ConnectionHandler.handle_messsage', f'unable to find request handler for "{message_type}" request', e, sep=' : ')
      return (False, {
        'type': 'error',
        'message': f'unable to find request handler for "{message_type}" request'
      })
      
    else:
      try:
        async with self.lock:
          return await message_handler(self, message)
      
      except Exception as e:
        print('ERROR', 'ConnectionHandler.handle_messsage', f'unexpected error occured while handle the "{message_type}" request', e, sep=' : ')
        return (False, {
          'type': 'error',
          'message': f'unexpected error occured while handle the "{message_type}" request'
        })
