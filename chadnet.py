#common functions, etc.
from bs4 import BeautifulSoup, NavigableString, Tag
from pathlib import Path

escapelist = {
  '&': '&amp;',
  '"': '&quot;',
  '<': '&lt;',
  '>': '&gt;',
  '’': "'",
  '‘': "'",
  '…': '...',
  '”': '&quot;',
  '“': '&quot;'
}

safe = ['br', 'hr']

def escape(text):
  return "".join(escapelist.get(c, c) for c in text)

def gold(text):
  print('\033[1;33m' + text + '\033[0m')

def getpath(filevar):
  return str(Path(filevar).resolve().parent)

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
    des = child.descendants
    for d in des:
      if d is None: #otherwise it seems to fail with NoneType
        clear = False
        break
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

