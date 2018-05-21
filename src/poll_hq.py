#!/usr/bin/env python
import requests
import ConfigParser
import json
import sys

config = ConfigParser.RawConfigParser()
config.read('hq.ini')

bearer_token = config.get('Main', 'bearer_token')

#print(bearer_token)
#sys.exit(1)

url='https://api-quiz.hype.space/shows/now'
h = {
    'User-Agent':'HQ-iOS/88 CFNetwork/808.2.16 Darwin/16.3.0',
    'x-hq-stk':'MQ==',
    'x-hq-device':'iPhone8,1',
    'Accept':'*/*',
    'Accept-Language':'en-us',
    'x-hq-client':'iOS/1.3.5 b88',
    'x-hq-test-key':'',
    'Authorization':'Bearer %s' % (bearer_token,)
}

print(requests.get(url, data={'type':'hq'}, headers=h).json())

