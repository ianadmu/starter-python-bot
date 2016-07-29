import urllib2
import random

def parseComicRequest(comicRequest):
	#This will give url to the desired comic
	maxComic = getCurrentMaxComic()
	minComic = 1
	url = "http://xkcd.org/"
	try:
		comicNumber = int(comicRequest)
		if(comicNumber >= minComic and comicNumber <= maxComic):
			return url + str(comicNumber) + '/'
	except:
		pass
	if comicRequest == "":
		return url

	comicNumber = random.randint(minComic,maxComic)
	return url + str(comicNumber) + '/'

def getImageLocation(comicRequest):

	response = urllib2.urlopen(parseComicRequest(comicRequest))
	html = response.read()

	imageAddressStart = html.find('//imgs.xkcd.com/comics/')
	imageAddressEnd = html[imageAddressStart:].find('"') + imageAddressStart
	imageAddress = html[imageAddressStart:imageAddressEnd]
	return "http:" + str(imageAddress)

def getCurrentMaxComic():
	response = urllib2.urlopen("http://xkcd.org/")
	html = response.read()

	identifierString = 'Permanent link to this comic: http://xkcd.com/'

	currentMaxStart = html.find(identifierString) + len(identifierString)
	currentMaxEnd = html[currentMaxStart:].find('/') + currentMaxStart
	return int(html[currentMaxStart:currentMaxEnd])