import streamlit as st
from PIL import Image
import torch
import torch.nn as nn
import pickle
import torchvision.transforms as transforms
from torchvision import models
import numpy as np
import cv2


#device = 'cuda' if torch.cuda.is_available() else 'cpu'
PATH = "EfficientNet_B4NO2Model.pt"
my_model = torch.load(PATH)#.to(device)
my_model.eval()

# Define a function to make predictions with the trained model
def predict(model, opencv_Image):
    # Load the image and transform it to the appropriate format
    transform = transforms.Compose([
        transforms.Resize((100, 100)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    #image = Image.open(image_path)
    pil_image = Image.fromarray(opencv_Image)
    image = transform(pil_image).unsqueeze(0)#.to(device)
    image = image

    # Make a prediction with the trained model
    #model.eval()
    with torch.no_grad():
        output = model(image)
        class_index = torch.argmax(output, dim=1).item()

    # Map the predicted index to the class name
    class_names = ['class1', 'class2', 'class3', 'class4']
    class_name = class_names[class_index]

    return class_name

tab1, tab2 = st.tabs(["Upload Image", "Capture Image"])

with tab1:
    test_image = st.file_uploader('Image', type=['jpg', 'png','jpeg', 'jfif'] )
    col1, col2 = st.columns(2)
    if test_image is not None:
        # Convert the file read to the bytes array.
        file_bytes = np.asarray(bytearray(test_image.read()), dtype=np.uint8)
        # Converting the byte array into opencv image. 0 for grayscale and 1 for bgr
        test_image_decoded = cv2.imdecode(file_bytes,1) 
        col1.subheader('Uploaded Test Image')
        col1.image(test_image_decoded, channels = "BGR")
        prediction = predict(my_model, test_image_decoded)
        col2.subheader('Predicted Class')
        col2.write(prediction)

with tab2:
    img_camera = st.camera_input("Capture Image")
    
    if img_camera is not None:
        # Convert the file read to the bytes array.
        file_bytes = np.asarray(bytearray(img_camera.read()), dtype=np.uint8)
        # Converting the byte array into opencv image. 0 for grayscale and 1 for bgr
        test_image_decoded = cv2.imdecode(file_bytes,1) 
        prediction = predict(my_model, test_image_decoded)
        st.subheader('Predicted Class')
        st.write(prediction)
