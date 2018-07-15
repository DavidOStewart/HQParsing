#!/usr/bin/env python
import requests
import ConfigParser
import json
import sys

from ws4py.client.threadedclient import WebSocketClient

class DummyClient(WebSocketClient):
  def closed(self, code, reason=None):
    print("Closed down", code, reason)

  def received_message(self, m):

    msg = json.loads(str(m))
    
    if 'type' in msg:
      if 'broadcastEnded' == msg['type']:
        self.close(reason='Broadcast Ended')

      elif 'question' == msg['type']:
        print("QUESTION:")
        print(msg['question'], msg['answers'])
        print("\n")

config = ConfigParser.RawConfigParser()
config.read('hq.ini')

url='https://api-quiz.hype.space/shows/now'
h = {
    'User-Agent': config.get('Main', 'user-agent'),
    'x-hq-stk':'MQ==',
    'x-hq-device': config.get('Main', 'x-hq-device'),
    'Accept':'*/*',
    'Accept-Language':'en-us',
    'x-hq-client': config.get('Main', 'x-hq-client'),
    'x-hq-test-key':'',
    'Authorization':'Bearer %s' % config.get('Main', 'bearer_token'),
}

response = requests.get(url, data={'type':'hq'}, headers=h).json()

if not response['broadcast']:
  print("No broadcast started.")
  sys.exit(0)


try:
  url = response['socketUrl'].replace('https', 'wss')
  h = {
    'User-Agent' : config.get('Main', 'user-agent'),
    'Authorization':'Bearer %s' % config.get('Main', 'bearer_token'),
    'x-hq-client' : config.get('Main', 'x_hq_client'),
  }
  ws = DummyClient(url, headers=h)
  ws.connect()
  ws.run_forever()
except KeyboardInterrupt:
  ws.close()

