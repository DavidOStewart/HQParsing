#!/usr/bin/env python
import requests

url_base = 'https://api-quiz.hype.space'
h = {
    'User-Agent': 'HQ-iOS/88 CFNetwork/808.2.16 Darwin/16.3.0',
    'x-hq-device': 'iPhone8,1',
    'Accept':'*/*',
    'Accept-Language':'en-us',
    'x-hq-client': 'iOS/1.3.5 b88',
    'x-hq-test-key':'',
}

phone = raw_input("Enter your phone number: ")
phone = phone.replace('-','')
phone = phone.replace('+','')

if len(phone) == 10:
  phone = '+1' + phone
else:
  phone = '+' + phone

v = {
  'method' : 'sms',
  'phone' : phone,
}

res = requests.post(url_base + '/verifications', data=v, headers=h).json()

v_id = res['verificationId']


code = raw_input("Enter the verification code (sent to you phone): ")
v = {
  'code' : code,
}

res = requests.post(url_base + '/verifications/'+v_id, data=v, headers=h).json()

print("Bearer Access Token:")
print(res['auth']['accessToken'])

