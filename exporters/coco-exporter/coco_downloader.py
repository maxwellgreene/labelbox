"""
Module for downloading a local copy of a labelbox dataset from MS COCO format.
"""
import coco_exporter
import main
import os

import json
import logging

from PIL import Image
import requests
import urllib.request

LOGGER = logging.getLogger(__name__)

def download_images(file_input,path_output):
    IMAGE_PATH = ('{}/images/'.format(path_output))

    if not os.path.exists(IMAGE_PATH):
      print("Creating directory: ",IMAGE_PATH)
      os.mkdir(IMAGE_PATH)

    #os.chdir(IMAGE_PATH)

    #specify final sizes
    width  = 1024
    height = 1024
    resize = True

    with open(file_input, 'r') as file_handle:
        data = json.loads(file_handle.read())

    for i, item in enumerate(data):
      #Create path names
      orig_path = os.path.join(IMAGE_PATH,item['ID'] + "_original.jpg")
      final_path = os.path.join(IMAGE_PATH,item['ID'] + ".jpg")

      #Download, if not already downloaded
      url = item['Labeled Data']

      if os.path.exists(orig_path):
        print("Item:",i," - NOT Downloading image   id: ",item['ID'])
      else:
        print("Item:",i," - Downloading image  with id: ",item['ID'], " to ",orig_path)
        urllib.request.urlretrieve(url,orig_path)

      #Load file as img
      if os.path.exists(final_path):
        #Get image from resized path
        img = Image.open(final_path).convert('RGB')
        if not (img.width == width and img.height == height):
          #If not resized, resize original again and resave
          img = Image.open(orig_path).convert('RGB')
          print("Item:",i," - Resizing to",width,"x",height,"id: ",item['ID'])
          img_resize = img.resize((width, height), Image.ANTIALIAS)
          img_resize.save(final_path)
        else:
          #If resized and proper size, do not resize
          print("Item:",i," - NOT resizing,  resized, id: ",item['ID'])
      else:
        #If no resize exists, load original to resize
        img = Image.open(orig_path).convert('RGB')
        if not (img.width == width and img.height == height):
          #IF original is not proper size, resize.
          print("Item:",i," - Resizing to",width,"x",height,"id: ",item['ID'])
          img_resize = img.resize((width, height), Image.ANTIALIAS)
          img_resize.save(final_path)
        else:
          print("Item:",i," - NOT resizing, already right:",width,"x",height,"id: ",item['ID'])
          img.save(final_path)

        ########## TODO: RESIZE MASKS ###########
