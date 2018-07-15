#!/usr/bin/env python

# import the necessary packages
from PIL import Image

import threading
import time
import pytesseract
import argparse
import requests
import unicodedata
from requests.utils import quote
import time
import re
import cv2
import os
import sys

start_time=time.time()

def googleSearch(question, answer, counter):

		counter+=1
		try:
			searchparam=question.replace(' ','+').replace('\n','+')+"+"+answer
			req = "https://www.google.com/search?q="+searchparam
			print(req)
			r = requests.get(req)
			print("Query took " + str(time.time() - start_time) + " seconds")
			print(chr(counter)+")", answer + " results:", re.search('\>About [0-9,]* results', str(r.text)).group(0).split(' ')[1])
			regex=question +" "+ answer
			print("Answer with spaces occurrences in response json: " + str(r.text.lower().count(regex.lower())))
			regex="[^\+\w]+"+answer.lower()+"[^\w]*"
			print("Answer with spaces occurrences in response json: " + str(re.subn(regex, '', str(r.text.lower()))[1]))
			regex="[^\+\w]"+answer2.lower()+"[^\w]*"
			print("Answer without spaces occurrences in response json: " + str(re.subn(regex, '', str(r.text.lower()))[1]) + "\n")
		except:
			print(chr(counter) + ") " + answer + " is not the answer for sure\n")
 

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
args = vars(ap.parse_args())

text = pytesseract.image_to_string(Image.open(args["image"]))
#print(text)

lines = text.split('\n\n', 1)
question = lines[0].replace("\n",' ')
question = unicodedata.normalize("NFKD", question)

print("Answers:\n")

counter = 96

print("Program ran in " + str(time.time() - start_time) + " seconds")	

for answer in lines[1].split("\n"):
	answer2=answer.replace(' ', '')
	if answer!="":
		threading.Thread(target=googleSearch,args=(question, answer, counter)).start()
		counter+=1
	
print("Program ran in " + str(time.time() - start_time) + " seconds")
