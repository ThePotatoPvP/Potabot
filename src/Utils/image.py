# -*- coding: utf-8 -*-

from PIL import Image, ImageSequence
import urllib.request
import re, os

def trans(x: int, y: int, W:int, H:int) -> bool:
    """
    W is the width of the image, H is the height
    (x,y) are the coordinates of the current pixel
    """
    return ((x-W/2)**2)/(5*W**2) + (y-H/0.216)**2/(14*H**2) <=1 \
    or ((x>(3*W)/4) and (y> (4*H/W)*x - 3*H/W - 2.35*H))

def booblify(img_name: str):
    im = Image.open(img_name)
    duration = im.info.get('duration', 100)
    new_frames = []
    for frame in ImageSequence.Iterator(im):
        frame = frame.convert('RGBA')
        new_frame = Image.new('RGBA', frame.size)
        for x in range(frame.size[0]):
            for y in range(frame.size[1]):
                if trans(x, frame.size[1]-y, frame.size[0], frame.size[1]):
                    pixel = frame.getpixel((x, y))
                    new_pixel = pixel[:-1] + (0,)
                    new_frame.putpixel((x, y), new_pixel)
                else:
                    new_frame.putpixel((x, y), frame.getpixel((x, y)))
        new_frames.append(new_frame)
    new_frames[0].save(img_name, format='GIF',
    append_images=new_frames[1:], save_all=True, duration=duration, loop=0)

def togif(path: str):
    with Image.open(path) as im:
        if im.format == 'GIF' and 'duration' in im.info:
            frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
            frames[0].save(path[:-4]+'.gif', format='GIF', append_images=frames[1:],
            save_all=True, duration=im.info['duration'], loop=0)
        else:
            im = im.convert('RGBA')
            im.save(path[:-4]+'.gif', format='GIF', save_all=True, duration=100, loop=0)
    if not path.endswith('.gif'):
        os.remove(path)

def tenorScrapper(link: str):
    """
    Returns the image link from a tenor share link
    """
    regex = r'https\:\/\/media\.tenor\.com\/[a-z,A-Z,0-9-]+\/[a-z,A-Z,0-9,-]+\.gif+'
    page = urllib.request.urlopen(link).read().decode()
    imgs = re.finditer(regex, page)
    return  [g.group(0) for g in imgs][0]