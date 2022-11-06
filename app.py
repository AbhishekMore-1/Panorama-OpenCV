# -*- coding: utf-8 -*-
# Import required libraries

import cv2
import numpy as np
import streamlit as st
import requests
import os

# Home UI 

def main():

    st.set_page_config(layout="wide")

    tabs = st.tabs(('About Me','Panorama Image'))

    # UI Options 
    with tabs[0]:
        aboutMe() 
    with tabs[1]:
        panorama()

# Pre-process Image
def preProcessImg(img):
    # Pre-processing image: resize image
    height, width, _ = img.shape
    width = int(720/height*width)
    height = 720
    img = cv2.resize(img,(width,height))
    return img

# Upload Image
def uploadImages(key):

    uploaded_files = st.file_uploader("Choose Image files in Proper sequence",key=key,accept_multiple_files=True)
    imgs = list()
    for file in uploaded_files:
        file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        # Pre-processing image: resize image
        imgs.append(preProcessImg(img))
    
    if imgs:
        return imgs
    
    img = cv2.cvtColor(preProcessImg(cv2.imread('sample.jpg')),cv2.COLOR_BGR2RGB)
    size = img.shape[1] - 1
    return [
        img[:,:int(1/2*size),:],
        img[:,int(1/4*size):int(3/4*size),:],
        img[:,int(1/2*size):,:]
    ]

# About Me UI 

def aboutMe():
    
    st.markdown(requests.get(os.getenv('ABOUT_ME','https://raw.githubusercontent.com/AbhishekMore-1/AbhishekMore-1/main/README.md')).text, unsafe_allow_html=True)

# Panorama 

def panorama():

    st.header("Panorama Image")

    imgs = uploadImages(0)

    # Original Image
    st.subheader("Original Images")

    original_imgs = st.columns(len(imgs))
    for (original_img,img) in zip(original_imgs,imgs):
        with original_img:
            st.image(img,use_column_width=True)

      
    st.subheader("Panorama Image")

    stitchy = cv2.Stitcher.create()
    ok,panorama =stitchy.stitch(imgs)

    if ok != cv2.STITCHER_OK:
    # checking if the stitching procedure is successful
    # .stitch() function returns a true value if stitching is
    # done successfully
        st.warning("Panorama is not possible for given images in given sequence!!!")
    else:
        st.image(panorama,use_column_width=True)

if __name__ == "__main__":
    main()