#!/usr/bin/python3
import time
import sys
import os
import pyperclip as clip
from chadnet import gold

def toggleparagraph():
  gold('CHADNET SYSTEM ALPHA: PARAGRAPH')
  return 1

def blockquotebegin():
  gold('CHADNET SYSTEM ALPHA: BLOCKQUOTE BEGIN')
  return 2

def blockquoteend():
  gold('CHADNET SYSTEM ALPHA: BLOCKQUOTE END')
  #end blockquote
  gold('CHADNET SYSTEM ALPHA: PARAGRAPH')
  return 1

def image():
  gold('CHADNET SYSTEM ALPHA: IMAGE')
  return 3

def caption():
  gold('CHADNET SYSTEM ALPHA: CAPTION')
  return 4

def ulbegin():
  gold('CHADNET SYSTEM ALPHA: UNORDERED LIST BEGIN')
  return 5

def ulend():
  gold('CHADNET SYSTEM ALPHA: UNORDERED LIST END')
  #end ul
  gold('CHADNET SYSTEM ALPHA: PARAGRAPH')
  return 1

def olbegin():
  gold('CHADNET SYSTEM ALPHA: ORDERED LIST BEGIN')
  return 6

def olend():
  gold('CHADNET SYSTEM ALPHA: ORDERED LIST END')
  #end ol
  gold('CHADNET SYSTEM ALPHA: PARAGRAPH')
  return 1

def showhelp():
  gold('CHADNET SYSTEM ALPHA: HELP')
  print('1 -- PARAGRAPH')
  print('2 -- BLOCKQUOTE BEGIN')
  print('3 -- BLOCKQUOTE END')
  print('4 -- IMAGE')
  print('5 -- CAPTION')
  print('6 -- UNORDERED LIST BEGIN')
  print('7 -- UNORDERED LIST END')
  print('8 -- ORDERED LIST BEGIN')
  print('9 -- ORDERED LIST END')
  print('0 -- STOP')
  print('- -- HELP')

def handletext(text):
  print('text: ' + text)

handlers = {
  'CHADNET_SYSTEM_ALPHA_PARAGRAPH': toggleparagraph,
  'CHADNET_SYSTEM_ALPHA_BLOCKQUOTE_BEGIN': blockquotebegin,
  'CHADNET_SYSTEM_ALPHA_BLOCKQUOTE_END': blockquoteend,
  'CHADNET_SYSTEM_ALPHA_IMAGE': image,
  'CHADNET_SYSTEM_ALPHA_CAPTION': caption,
  'CHADNET_SYSTEM_ALPHA_UNORDERED_LIST_BEGIN': ulbegin,
  'CHADNET_SYSTEM_ALPHA_UNORDERED_LIST_END': ulend,
  'CHADNET_SYSTEM_ALPHA_ORDERED_LIST_BEGIN': olbegin,
  'CHADNET_SYSTEM_ALPHA_ORDERED_LIST_END': olend,
  'CHADNET_SYSTEM_ALPHA_HELP': showhelp
}

clipboard = ""
clip.copy('')
while True:
  clipboard = clip.paste()
  if clipboard:
    handler = handlers.get(clipboard)
    if handler:
      mode = handler()
    else:
      handletext(clipboard)
  clip.copy('')
  time.sleep(0.1)
