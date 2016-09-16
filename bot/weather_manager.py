#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import random
from HTMLParser import HTMLParser
import re
import ssl
 
def scrapeItem(html, startString, endString, parser):
	start = html.find(startString) + len(startString)
	end = html[start:].find(endString) + start
	return parser.unescape(html[start:end])

def getCurrentWeather():
	ssl._create_default_https_context = ssl._create_unverified_context
	stringsBeforeGT = re.compile("(\n|.)*>")
	url = "https://weather.gc.ca/city/pages/mb-38_metric_e.html"
	conditionString = 'Condition:'
	temperatureString = 'Temperature:'
	temperatureEnd = '&deg;'
	end = '</dd>'
	parser = HTMLParser()

	response = urllib2.urlopen(url)
	html = response.read()

	condition = scrapeItem(html, conditionString, end, parser)
	temperature = scrapeItem(html, temperatureString, temperatureEnd, parser)
	#these need additional scraping
	condition = re.sub(stringsBeforeGT, "", condition)
	temperature = re.sub(stringsBeforeGT, "", temperature)

	return "It is currently " + temperature + "°C and " + condition