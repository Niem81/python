
# import libraries
import urllib2
import urllib
import os, sys
import requests
import shutil
from bs4 import BeautifulSoup

# another way of parsing the data from the url
from lxml import html

print 'Welcome to this PY file for scrapping and downloading images'
print 'You will select the Search Engine of your preference or Provide your own by selecting number 4'

print '1. Google Chrome'
print '2. Bing'
print '3. DuckDuckGo'
print '4. Enter Own URL'

motor = raw_input('Enter number of Your Option: ')

if motor == '1':
    url = 'http://www.google.com/search?hl=en&gl=us&authuser=0&q=%(query)s'
elif motor == '2':
    url = 'http://www.google.com/search?hl=en&gl=us&authuser=0&q=%(query)s'
elif motor == '3':
    url = 'http://www.google.com/search?hl=en&gl=us&authuser=0&q=%(query)s'
elif motor == '4':
    url = raw_input('Enter your URL or link that you would like to get the images from: ')

# querying the website and return the html to the variable 'page'
# page = urllib.urlopen(url)
page = requests.get(url)
print page
print page.status_code

tree = html.fromstring(page.content)
print tree

# parsing the html using beautiful soap and store in variable 'soup'
soup = BeautifulSoup(page.content)
soup.prettify()
print soup

# getting images into an array
images = [img for img in soup.findAll('img')]

# set to the selected folder
# Create a directory
directoryName = raw_input('Enter new directory name: ')
cmdToExecute = 'mkdir ' + directoryName
print cmdToExecute
os.popen(cmdToExecute)

# Change Directory
directoryPath = os.getcwd()
print directoryPath, directoryName
directoryPath = os.path.join(directoryPath, directoryName)
os.chdir(directoryPath)
print os.getcwd()

print 'Downloading images to current working directory'

image_links = [each.get('src') for each in images]
print image_links

if page.status_code == 200:
	for each in image_links:
		print each
		filename=each.split('/')[-1]
		# filename = filename + ".jpg"
		if filename[-3:] != "jpg":
			pass
		else:
			each_src = "https:" + each
			img_link = requests.get(each_src, stream=True)
			print img_link.status_code
			with open(filename, 'wb') as f:
				# f.write(each)
				print filename
				img_link.raw.decode_content = True
				shutil.copyfileobj(img_link.raw, f)
	
print 'Finish getting images'