#!/usr/bin/env python
#
#   Copyright (C) 2017 Sean D'Epagnier
#
# This Program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.  

from sys import stdout
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageChops


def create_character(n, c, ifont):
    size = ifont.getsize(c)
    image = Image.new('RGBA', size)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), c, font=ifont)
    data = list(image.getdata())
    print 'const PROGMEM unsigned char font%d_%02x[] = {' % (n, ord(c))
    for i in range(len(data)):
        stdout.write('0x%02x, ' % data[i][0])
    print '};';
    return size

def create_font(n, param):
    ifont = ImageFont.truetype("font.ttf", param[1])
    sizes = {}
    for c in param[0]:
        sizes[c] = create_character(n, c, ifont)
    print 'const PROGMEM struct font_character font%d[] = {' % n
    for c in param[0]:
        print '{%d, %d, %d, font%d_%02x},' % (ord(c), sizes[c][0], sizes[c][1], n, ord(c))
    print '};'

def create_fonts(params):
    n = 0
    for param in params:
        create_font(n, param)
        n = n+1
    print 'const PROGMEM struct font fonts[] = {'
    for i in range(n):
        print '{%d, font%d},' % (len(params[i][0]), i)
    print '};'

print '// This file is generated by make_charset.py'
print ''
print 'struct font_character {'
print '    char c;'
print '    uint8_t w, h;'
print '    const unsigned char *data;'
print '};'

print 'struct font {'
print '    uint8_t n;'
print '    const struct font_character *characters;'
print '};'

numeric = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
alpha = map(lambda x : '%c' % x, range(ord('A'), ord('Z') + 1))
lower = map(lambda x : '%c' % (ord(x) + 32), alpha)

create_fonts([(numeric + list('C.'), 12), (numeric, 14), (numeric, 16), (numeric, 24)])
