#-*- coding:utf-8 -*-
import os
import random
import uuid

from PIL import Image, ImageDraw, ImageFont, ImageFilter


CODE_ROOT   = os.path.dirname(__file__)


LETTER_CASES = 'abcdefghijklmnopqrstuvwxyz'
UPPER_CASES  = LETTER_CASES.upper()
NUMBER_CASES = ''.join(map(str,range(10)))
DEFAULT_CHARS = ''.join((LETTER_CASES, UPPER_CASES, NUMBER_CASES))

DEFAULT_FONT_TYPE = os.path.normpath(os.path.join(CODE_ROOT, '','fonts/courbd.ttf'))
DEFAULT_FONT_SIZE = 32
DEFAULT_FONT = ImageFont.truetype(DEFAULT_FONT_TYPE,DEFAULT_FONT_SIZE)

class Captcha(object):
  def __init__(self, size=(120,40), chars = DEFAULT_CHARS,
               bg_color=(255,255,255), fg_color=(80,80,80),length=6):
    if len(size) !=2: raise 'size: error'
    self.width    = size[0]
    self.height   = size[1]
    self.chars    = chars
    self.bg_color = bg_color
    self.fg_color = fg_color
    self.length   = length

    self.img      = Image.new('RGB',size,bg_color)
    self.draw     = ImageDraw.Draw(self.img)

  def save(self, ROOT = './'):
    self.img.save(ROOT+str(uuid.uuid1())+'.png','png')

  def drawLines(self, min_lines=4,max_lines=10):
    line_num    = random.randint(min_lines,max_lines)
    for i in range(line_num):
      begin     = (random.randint(0,self.width), random.randint(0,self.height))
      end       = (random.randint(0,self.width), random.randint(0,self.height))

      self.draw.line([begin, end], fill=self.fg_color)
  def drawPoints(self,point_chance=20):
    '''
    point_chance 干扰点的百分比
    '''
    chance      = min(100, max(0,int(point_chance)))
    for x in xrange(self.width):
      for y in xrange(self.height):
        temp    = random.randint(0,100)
        color   = (random.randint(0,125), random.randint(0,125), random.randint(0,125))
        if temp > 100 - chance:
          self.draw.point((x,y), fill=color)

  def drawString(self):
    code_chars  = random.sample(self.chars,self.length)
    code_strs   = '%s' % ''.join(code_chars)
    font_width, font_height = DEFAULT_FONT.getsize(code_strs)
    char_width = font_width / self.length
    startx = self.width / self.length - char_width
    if startx <= 0 : startx = random.randint(0,self.width / self.length / 2)
    for i in xrange(self.length):
      starty    = random.randint(0,(self.height - font_height)/2)
      self.draw.text((startx, starty), code_strs[i], font=DEFAULT_FONT, fill=self.fg_color)
      startx   += char_width
    return code_strs

  def captcha(self, min_lines=4,max_lines=10, point_chance=20):
    code_strs  = self.drawString()
    self.drawLines(min_lines,max_lines)
    self.drawPoints(point_chance)
    return code_strs
    
if __name__ == '__main__':
  code = Captcha()
  code_strs = code.captcha()
  code.save()
  print code_strs
