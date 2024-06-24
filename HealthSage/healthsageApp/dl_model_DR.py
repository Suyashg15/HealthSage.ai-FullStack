from django.shortcuts import render
from django.http import JsonResponse
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import io
from PIL import Image

model = load_model('models/resnet18.h5')

labels = {0:'Mild',1:'Moderate',2:'No_DR',3:'Proliferate_DR', 4:'Severe'}
def class_name(classno):
    if classno==0:
        return "Mild Diabetic Retinopathy"
    elif classno==1:
        return "Moderate Diabetic Retinopathy"
    elif classno==2:
        return "Healthy"
    elif classno==3:
        return "Proliferate Diabetic Retinopathy"
    else:
        return "Severe Diabetic Retinopathy"
    
def preprocess_image(image_path):
    image = load_img(image_path, target_size=(256, 256))
    # image = image.resize((256, 256))5-xvhk
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0  # Normalize the image
    prediction = model.predict(image)
    predicted_class = np.argmax(prediction, axis=1)
    return predicted_class[0]

    # img = image.load_img(image_path, target_size=(256, 256))
    # img_array = image.img_to_array(img)
    # img_array = np.expand_dims(img_array, axis=0)
    # predictions = model.predict(img_array)
    # predicted_class = np.argmax(predictions, axis=1)[0]
    # return predicted_class

    