#!/usr/bin/python3
from unidecode import unidecode
from natsort import natsorted, ns
from operator import itemgetter
from chadnet import escape, gold, getpath
from subprocess import call
from shutil import copyfile

location = getpath(__file__)

def getlinks(filename):
  with open(filename, 'r') as f:
    pos = 1
    links = []
    for line in f:
      if pos % 5 == 1: #TITLE
        title = line.strip()
      elif pos % 5 == 2: #URL
        url = line.strip()
      elif pos % 5 == 3: #CATEGORIES
        cats = [x.strip() for x in line.strip().split(',')]
      elif pos % 5 == 4: #DESCRIPTION
        desc = line.strip()
      elif pos % 5 == 0: #BLANK
        links.append([title, url, cats, desc])
      pos += 1
  return links

def getcats(filename):
  with open(filename, 'r') as f:
    pos = 1
    cats = []
    for line in f:
      if pos % 4 == 1: #TITLE
        title = line.strip()
      elif pos % 4 == 2: #URL
        url = line.strip()
      elif pos % 4 == 3: #PARENTS
        parents = [x.strip() for x in line.strip().split(',')]
      elif pos % 4 == 0: #BLANK
        cats.append([title, url, parents])
      pos += 1
  return cats

def ignore(text, safelist):
  text = unidecode(text).lower()
  for i in text:
    if i.isalnum() == True or i in safelist:
      continue
    else:
      text = text.replace(i, '')
  #print(text)
  return ' '.join(text.split())

def sortlist(thelist):
  return natsorted(thelist, key=lambda x: ignore(x[0], [' ']))

def writedb(filename, thelist):
  with open(filename, 'w') as f:
    for entry in thelist:
      for line in entry:
        if isinstance(line, list):
          f.write(", ".join(str(item) for item in line) + '\n')
        else:
          f.write(line + '\n')
      f.write('\n')

def joindb(cats, links):
  for cat in cats:
    cat.append([])
    cat.append([])
    for cat2 in cats:
      for parent in cat2[2]:
        if cat[1] == parent:
          #print(cat[1])
          #print("in: " + str(cat2[1]))
          cat[3].append(cat2[:2])

  for link in links:
    for cat in link[2]:
      for category in cats:
        if cat == category[1]:
          category[4].append(link)
  return cats

def getlinkicon(url):
  if url.startswith('http') is True:
    if url.startswith('https://www.youtube.com'):
      image = 'yt.svg'
    else:
      image = 'globe.svg'
  elif url.startswith('files') is True:
    if url.endswith(('jpg', 'jpeg', 'png', 'gif')) is True:
      image = 'painting.png'
    elif url.endswith(('mp4', 'webm')) is True:
      image = 'video.png'
    elif url.endswith('mp3') is True:
      image = 'speaker.png'
    else:
      image = 'doc.png'
  else:
    image = 'chad-square.png'
  return image

def makecats(cats):
  with open(f'{location}/templates/HEAD_CAT', 'r') as head:
    for cat in cats:
      #print(cat[1])
      with open(f'{location}/../' + cat[1] + '.html', 'w') as f:
        head.seek(0)
        for line in head:
          f.write(line.replace('CHADNET_SYSTEM_ALPHA_TITLE', escape(cat[0])).replace('CHADNET_SYSTEM_ALPHA_LINKS', str(len(cat[4]))))
        f.write('  <ul class="category">\n')
        #print(cat[3])
        for linkedcat in cat[3]:
          #print('cat[3]: ' + str(cat[3]))
          #speed test!
          #print('linkedcat: ' + str(linkedcat))
          for othercat in cats:
            if linkedcat[1] == othercat[1]:
              catcats = len(othercat[3])
              catlinks = len(othercat[4])
          f.write(f'    <li><img src="folder.png" draggable="false"><a href="{linkedcat[1]}.html">{escape(linkedcat[0])}</a>')
          catimg = '<img src="folder.png" draggable="false" class="stats">'
          linkimg =  '<img src="link.png" draggable="false" class="stats">'
          if catcats > 0 and catlinks > 0:
            f.write(f' ({catcats} {catimg} {catlinks} {linkimg})')
          elif catcats == 0 and catlinks > 0:
            f.write(f' ({catlinks} {linkimg})')
          elif catcats > 0 and catlinks == 0:
            f.write(f' ({catcats} {catimg})')
          f.write('</li>\n')
        for link in cat[4]:
          url = link[1]
          if url[0] == '!':
            target = True
            url = url[1:]
          else:
            target = False
          image = getlinkicon(url)
          f.write(f'    <li><img src="{image}" draggable="false"><a href="{url}"')
          if target is True:
            f.write(' target="_blank"')
          f.write(f'>{escape(link[0])}</a>')
          if link[3] != '':
            f.write(f' {escape(link[3])}')
          f.write('</li>\n')
        f.write('  </ul>\n</body>\n</html>')

def wrapsearch(text):
  return '"' + text.replace('\\"', '"').replace('"', '\\"') + '",\n' #schizophrenia

def convertsearch(text):
  text.replace('&', 'and')
  return ignore(text, ['/', ' '])

def makesearch(links):
  with open(f'{location}/../search.html', 'w') as f:
    with open(f'{location}/templates/HEAD_SEARCH', 'r') as head:
      for line in head:
        f.write(line)
    for link in links:
      #title = link[0]
      f.write(wrapsearch(convertsearch(link[0])))
      f.write(wrapsearch(link[0]))
      #desc = link[3]
      f.write(wrapsearch(convertsearch(link[3])))
      f.write(wrapsearch(link[3]))
      url = link[1]
      if url[0] == '!':
        target = True
        url = url[1:]
      else:
        target = False
      f.write(wrapsearch(url))
      f.write(wrapsearch(getlinkicon(url)))
      if target is True:
        f.write('"1",\n')
      else:
        f.write('"0",\n')
    f.write('];\n</script>\n</body>\n</html>')


gold("CHADNET SYSTEM ALPHA: WIKI SYSTEM v3.0")
copyfile(f'{location}/../db.chad', f'{location}/backups/db.chad')
links = getlinks(f'{location}/../db.chad')
links = sortlist(links)
linkcount = len(links)
writedb(f'{location}/../db.chad', links)
print("Sorted db.chad")
cats = getcats(f'{location}/../cat.chad')
cats = sortlist(cats)
catcount = len(cats)
writedb(f'{location}/../cat.chad', cats)
print("Sorted cat.chad")
print("Links: " + str(linkcount))
print("Categories: " + str(catcount))
with open(f'{location}/CHADNET_LINK_COUNT', 'w') as f:
  f.write(str("{:,}".format(linkcount)))
rc = call(f'{location}/update.sh')
print("Updated index.html")

cats = joindb(cats, links)
#print(cats)
makecats(cats)
print("Created categories")

makesearch(links)
print("Set up search")
