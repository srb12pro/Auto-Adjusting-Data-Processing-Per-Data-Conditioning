#!/usr/bin/env python
# coding: utf-8

# In[1]:


from ultralytics import YOLO
import os
import numpy as np
import pandas as pd
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import torch
from pathlib import Path


# In[36]:


# Loading the pre-trained model
model = YOLO('yolov8x.pt')


# In[37]:


# Defining a function for object detection
def detect_objects(image_path):
    # Loading the image
    img = cv2.imread(str(image_path))

    # Running object detection on image
    results = model(img)
    
    # Extracting the classes and their ID dictionary 
    class_dict=model.names

    # Extracting class labels and confidence scores
    for r in results:
        labels = r[:].boxes.cls
        scores=r[:].boxes.conf
        
    # Convert tensor output to Python list
    cls_lst = labels.tolist()
    conf_lst=scores.tolist()
    
    # Rounding the numbers
    conf_lst = [round(num, 2) for num in conf_lst]
    
    # Creating a list concatenating class name and their respective confidence scores
    class_list = [class_dict.get(item, item) for item in cls_lst]
    f_list = [classes + ':' + str(conf) for classes, conf in zip(class_list, conf_lst)]

    return f_list


# In[38]:


# Defining function to run object detection on a folder of images
def img_directory(dir_path):
    # Get list of image paths
    image_paths = list(dir_path.glob('*.png'))

    # Initialize results dataframe
    df = pd.DataFrame(columns=['image_name', 'class_score'])

    # Process each image in directory
    for image_path in image_paths:
        # Image name
        image_name = image_path.stem

        # Running object detection on image
        class_score = detect_objects(image_path)

        # Add results to dataframe
        df = df.append({'image_name': image_name, 'class_score': class_score}, ignore_index=True)

    return df


# In[39]:


# Running the entire algo
images_path = Path('/Users/ananthkumarkanaparthy/Downloads/AlphaISP - Denoising Dataset/PNG Data/2DNR Denoising/Ground Truth' )
results = img_directory(images_path)
print(results.head(5))

