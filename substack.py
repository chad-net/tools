#!/usr/bin/python3
from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import os
import sys
import re
from urllib.parse import urlparse
import random, string
import datetime
from chadnet import escape, gold, getpath

location = getpath(__file__)

image = False

months = {
  "01": "January",
  "02": "February",
  "03": "March",
  "04": "April",
  "05": "May",
  "06": "June",
  "07": "July",
  "08": "August",
  "09": "September",
  "10": "October",
  "11": "November",
  "12": "December"
}

goodtags = ['a', 'p', 'strong', 'b', 'em', 'i', 'ul', 'ol', 'li', 'br', 'blockquote', 'q', 's', 'del', 'code', 'pre']
safe = ['br', 'hr']

def getfilename(url):
  filename = url.split('/')[-1] + ".html"
  if os.path.isfile('out/' + filename):
    print("File " + filename + " already exists")
    quit()
  return filename

def downloadpage(url):
  getfilename(url)
  source = requests.get(url).text
  soup = BeautifulSoup(source, 'lxml')
  return soup

def geturl():
  if len(sys.argv) > 1:
    url = sys.argv[1]
  else:
    print("No URL given")
    quit()
  return url

def gettitle(soup):
  return soup.find('h1', class_='post-title').text

def getsubtitle(soup):
  subtitle = soup.find('h3', class_='subtitle')
  if subtitle is not None:
    return subtitle.text
  else:
    return None

def getdate(soup):
  date = str(soup.find('div', class_='publish-context').time.attrs['datetime']).split('-')
  return months.get(date[1]) + " " + re.sub('^0', '', date[2].split('T')[0]) + ", " + date[0]

def getauthor(soup):
  author = soup.find('span', class_='byline-names').div.div.a.text
  return author

def getauthorurl(url):
  return "https://" + url.split('/')[-3] + "/"

def removeattrs(tag, soup):
  target = True
  if tag.name != 'a':
    tag.attrs = {}
  else:
    attrs = dict(tag.attrs)
    for attr in attrs:
      if attr == 'class':
        if tag['class'][0] == 'footnote-anchor':
          tag.attrs['href'] = '#' + tag.text
          tag.wrap(soup.new_tag('sup'))
          target = False
          if 'target' in attrs:
            del tag.attrs['target']
        del tag.attrs[attr]
      elif attr != 'href':
        del tag.attrs[attr]
    if target is True:
      tag.attrs['target'] = '_blank'
  return tag

def deldescendantattrs(soup, realsoup):
  if soup is None:
    return None
  soup = removeattrs(soup, realsoup)
  for child in soup.descendants:
    if isinstance(child, Tag):
      child = removeattrs(child, realsoup)
  return soup

def deltags(soup):
  for tag in soup.findAll(True):
    if tag.name not in goodtags:
      tag.unwrap()
  return soup

def handletag(soup, realsoup):
  soup = deldescendantattrs(delemptytags(deltags(soup), realsoup), realsoup)
  return contentcheck(soup)

def contentcheck(soup):
  if soup is None:
    return None
  if len(soup.contents) > 0: # this must be improved
    return soup
  else:
    return None

def writetofile(text, f):
  if text is not None:
    f.write("  " + str(text) + "\n")

def downloadimg(url):
  try:
    imgdata = requests.get(url).content
  except Exception as e:
    print("Could not download image: " + str(e))
    return None
  path = urlparse(url).path
  ext = os.path.splitext(path)[1]
  name = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + ext
  imgname = "out/files/" + name
  print("IMG: " + imgname)
  with open(f'{location}/{imgname}', 'wb') as handler:
    handler.write(imgdata)
  return "files/" + name

def handleimg(child, soup, f):
  global image
  img = downloadimg(child.figure.a.attrs['href'])
  if image is True:
    writetofile("<br>", f)
  writetofile('<a href="' + img+ '" target="_blank"><img class="center" src="' + img + '"></a>', f)
  captiontag = child.figure.find('figcaption')
  if captiontag is not None:
    caption = handletag(captiontag, soup)
    caption.name = 'p'
    caption['class'] = 'c'
    writetofile(caption, f)
  else:
    image = True

def handleheader(child, soup, f):
  new = handletag(child, soup)
  if new.name == 'h1':
    new.name = 'h2'
  writetofile(new, f)

def handlepullquote(child, soup, f):
  pullquote = handletag(child, soup)
  pullquote.name = 'blockquote'
  writetofile(pullquote, f)

def handlefootnote(child, soup, f):
  if child.name != 'div':
    return
  footnote = handletag(child.div.p, soup)
  footnote.string = " " + str(footnote.string)
  number = soup.new_tag("sup")
  number.attrs['id'] = child.a.text
  number.string = child.a.text
  footnote.insert(0, number)
  writetofile(footnote, f)

def delemptytags(child, soup):
  if child is None:
    return None
  if len(child.contents) == 0:
    return None
  for content in child.contents:
    if str(content).isspace():
      content.extract()
  clear = False
  while clear is False:
    clear = True
    for d in child.descendants:
      if isinstance(d, NavigableString):
        continue
      if d.name in safe:
        continue
      if len(d.contents) == 0:
        clear = False
        d.extract()
        continue
      for content in d.contents:
        if str(content).isspace():
          clear = False
          content.extract()
  if len(child.contents) == 0:
    return None
  return child

handlers = {
  'captioned-image-container': handleimg,
  'header-with-anchor-widget': handleheader,
  'pullquote': handlepullquote,
  'footnote': handlefootnote
}

url = geturl()
soup = downloadpage(url)
filename = getfilename(url)
gold('CHADNET SYSTEM ALPHA: SUBSTACK v1.1')
print('URL:        ' + url)
title = gettitle(soup)
escapedtitle = escape(title)
print('File:       ' + filename)
print('Title:      ' + title)
subtitle = getsubtitle(soup)
if subtitle is not None:
  print('Subtitle:   ' + str(subtitle))
date = getdate(soup)
print('Date:       ' + date)
author = getauthor(soup)
escapedauthor = escape(author)
print('Author:     ' + author)
authorurl = getauthorurl(url)
print('Author URL: ' + authorurl)
print('View:\nfile://' + os.path.abspath('out/' + filename))
print('------------------')
db = open(f'{location}/db', 'a')
print(title)
db.write(title + "\n")
print(filename)
db.write(filename + "\n")
time = datetime.datetime.now()
print(", " + time.strftime("%b").lower() + str(time.year))
db.write(", " + time.strftime("%b").lower() + str(time.year) + "\n")
print("by " + author)
db.write("by " + author + "\n\n")
db.close()
print('------------------')

f = open(f'{location}/out/' + filename, 'w')

if subtitle is not None:
  head = "templates/HEAD_SUBTITLE"
else:
  head = "templates/HEAD"

with open(f'{location}/{head}', 'r') as headfile:
  for line in headfile:
    f.write(line.replace('CHADNET_SYSTEM_ALPHA_TITLE', escapedtitle).replace('CHADNET_SYSTEM_ALPHA_SUBTITLE', str(subtitle)))

writetofile('<!-- This article was generated automatically using Chadnet System Alpha: SUBSTACK v1.0. If there are any stylistic errors or bugs, please report them. -->', f)
writetofile('<p>From the <a href="' + url + '" target="_blank">original article</a> on ' + date + ', by <a href="' + authorurl + '" target="_blank">' + escapedauthor + '</a>.</p>',f)

text = soup.find('div', class_='available-content')
for child in text.div.children:
  if isinstance(child, NavigableString):
    continue

  if isinstance(child, Tag):
    if child.has_attr('class'):
      childclass = child['class'][0]
      handler = handlers.get(childclass)
      if handler:
        if childclass != 'captioned-image-container':
          image = False
        handler(child, soup, f)
        continue

    if child.name in ['p', 'ul', 'ol', 'blockquote', 'pre']:
      image = False
      writetofile(handletag(child, soup), f)

f.write('</body>\n</html>')
f.close()
