import numpy as np
from PIL import Image
import cv2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Flatten, Dense, Dropout
from tensorflow.keras.applications.vgg19 import VGG19
# from tensorflow.keras.preprocessing.image import img_to_array, load_img


# Load the model
base_model = VGG19(include_top=False, input_shape=(128, 128, 3))
x = base_model.output
flat = Flatten()(x)
class_1 = Dense(4608, activation='relu')(flat)
drop_out = Dropout(0.2)(class_1)
class_2 = Dense(1152, activation='relu')(drop_out)
output = Dense(2, activation='softmax')(class_2)
model_03 = Model(base_model.inputs, output)
model_03.load_weights('models/vgg19_unfrozen.h5')

def get_className(classNo):
    print(classNo)
    if classNo == 0:
        return "Normal"
    elif classNo == 1:
        return "Pneumonia"

def getResult(img):
    image=cv2.imread(img)
    image = Image.fromarray(image, 'RGB')
    image = image.resize((128, 128))
    image=np.array(image)
    input_img = np.expand_dims(image, axis=0)
    input_img = input_img.astype('float32') / 255.0
    result=model_03.predict(input_img)
    result01=np.argmax(result,axis=1)
    return result01


