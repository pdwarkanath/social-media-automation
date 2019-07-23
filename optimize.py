import os
from PIL import Image
from shutil import copyfile
import sys


def compressMe(filename, meme, verbose=False):
    if (os.path.splitext(filename)[1].lower() == '.gif') or (os.path.splitext(filename)[1].lower() == '.mp4'):
        return
    filepath = os.path.join('C:\\Hugo\\weekinmemes\\static\\img', meme, filename)
    copyfilepath = os.path.join(os.getcwd(),'img', meme, filename)
    newfilepath = os.path.join(os.getcwd(),'img_compressed', meme, filename)
    
    oldsize = os.stat(filepath).st_size
    try:
        picture = Image.open(filepath)
    except OSError:
        return
    rgb_pic = picture.convert('RGB')
    dim = picture.size

    try:
        copyfile(filepath, copyfilepath)
        rgb_pic.save(newfilepath,"JPEG",optimize=True,quality=85)
    except FileNotFoundError:
        copy_dir = os.path.split(copyfilepath)[0]
        os.mkdir(copy_dir)
        copyfile(filepath, copyfilepath)
        
        new_dir = os.path.split(newfilepath)[0]        
        os.mkdir(new_dir)
        rgb_pic.save(newfilepath,"JPEG",optimize=True,quality=85)
    newsize = os.stat(newfilepath).st_size
    percent = (oldsize-newsize)/float(oldsize)*100
    if (verbose):
        print(f'File compressed from {oldsize} to {newsize} or {percent}')
    return percent

meme = sys.argv[1]
meme_path = os.path.join('C:\\Hugo\\weekinmemes\\static','img', meme)

files = os.listdir(meme_path)
for file in files:
    compressMe(file, meme, verbose=True)

