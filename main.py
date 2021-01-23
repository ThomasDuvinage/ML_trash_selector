import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import time
import cv2

import serial

from utils.Camera import *

camera = Camera()

arduino = serial.Serial(port="/dev/tty.usbmodem143101", baudrate=9600) # create usb link
time.sleep(2)#time recommended by arduino

classes = ["verre", "plastique et metal","carton", "rien"] #object classes 

# Scientific notation desactivation
np.set_printoptions(suppress=True)

# Importe model generated with teachablemachine
model = tensorflow.keras.models.load_model('keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


def predict_object(image_cv2):
    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)

    image_pil = Image.fromarray(image_cv2)
    image = image_pil.resize(size)

    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)

    indice_obj = np.argmax(prediction[0]) #highest prediction
    percentage = np.max(prediction[0]) * 100

    classe_detectee = classes[indice_obj]

    if percentage > 80:
        print("L'objet est : ", classe_detectee)
        print("Pourcentage : ", percentage, " %")

        return indice_obj #return index of the object in the classes array 
    else:
        print("Le pourcentage est trop faible")

    return None

def sendCommandArduino(classe_objet):
        arduino.write(str(classe_objet).encode('ascii'))#encode object class string to ascii  

            
while(True): #boucle infinie

    camera.capture()#take a picture of the scene 

    image_cv2 = cv2.imread("images/photo.jpg")#read captured image 

    objet = predict_object(image_cv2)#prediction de l'objet en fonction de la photo 

    if objet is not None: #if there is no problem with object prediction
        sendCommandArduino(objet)# send command to arduino
        time.sleep(2)#wait 2 seconds 
