from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from PIL import Image
from PIL.ExifTags import TAGS
import os
from urllib.parse import urlparse
import hashlib

description = "Micro services to process image"
app = FastAPI(
    title="Image Processing Service",
    description=description,
)

#-----COMMON CONFIG --

class Config():
    def storage(self):
        return 'Files'

#---- MODEL ---------
class GetUrl(BaseModel):
    url: str


#---- PROCESS -------
class File():
    
    def download(self,url):
        config_obj = Config()
        a = urlparse(url)
        r = requests.get(url, allow_redirects=True)
        file_name = os.path.basename(a.path)
        open(str(config_obj.storage())+"/"+file_name, 'wb').write(r.content)
        return str(config_obj.storage())+"/"+file_name
    
    def get_exif(self,file_name):
        imagename = file_name
        # read the image data using PIL
        image = Image.open(imagename)

        # extract other basic metadata
        info_dict = {
            "Filename": image.filename,
            "Image Size": image.size,
            "Image Height": image.height,
            "Image Width": image.width,
            "Image Format": image.format,
            "Image Mode": image.mode,
            "Image is Animated": getattr(image, "is_animated", False),
            "Frames in Image": getattr(image, "n_frames", 1)
        }

        return info_dict



#------ ROUTES --------
@app.post('/get/exif',
description="This is the api to get the exif data of an image")
def getExifdata(url_info: GetUrl):
    file_url = url_info.url
    file_obj = File()
    file_name = file_obj.download(file_url)
    return file_obj.get_exif(file_name)
    
