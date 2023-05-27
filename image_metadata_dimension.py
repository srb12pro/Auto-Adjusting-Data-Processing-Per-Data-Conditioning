#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def image_dimension(path):
    from PIL import Image
    from PIL.ExifTags import TAGS
    import os
    import pandas as pd
 
    # Get the list of all files and directories
    file_list = os.listdir(path)
    
    info_dict = {
        "Filename": [],
        "Image Size": [],
        "Image Height": [],
        "Image Width": [],
        "Image Format": [],
        "Image Mode": [],
        "Image is Animated": [],
        "Frames in Image": [],
    }

    for i in file_list:
        # path to the image or video
        imagename = path + "/" + i

        # read the image data using PIL
        image = Image.open(imagename)

        info_dict["Filename"].append(i)
        info_dict["Image Size"].append(image.size)
        info_dict["Image Height"].append(image.height)
        info_dict["Image Width"].append(image.width)
        info_dict["Image Format"].append(image.format)
        info_dict["Image Mode"].append(image.mode)
        info_dict["Image is Animated"].append(getattr(image, "is_animated", False))
        info_dict["Frames in Image"].append(getattr(image, "n_frames", 1))
    
    image_dim = pd.DataFrame.from_dict(info_dict)
    
    return(image_dim)

#path2 = 'D:/Work/GMU-US/4_Spring 2023/DAEN_690/Dataset/Denoising Dataset/AlphaISP - Denoising Dataset/AlphaISP - Denoising Dataset/PNG Data/2DNR Denoising/Ground Truth'
#image_dim = image_dimension(path2)
#print(image_dim.head())