#common functions, etc.
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

def escape(text):
  return "".join(escapelist.get(c, c) for c in text)

def gold(text):
  print('\033[1;33m' + text + '\033[0m')

def getpath(filevar):
  return str(Path(filevar).resolve().parent)
