from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
import argparse

print("begin")
parser = argparse.ArgumentParser(description = 'Uses saved weights from a Keras CNN to classify images')
parser.add_argument('model_file', metavar = 'model', type = str, help = 'the file path to the model weight h5 file')
parser.add_argument('image_file', metavar = 'image', type = str, help = 'the file path to the image file to be classified')
args = parser.parse_args()
#print(args.model_weights)
#print(args.image_file)

weights = args.model_file
image = args.image_file

model = load_model(weights)

def output_prediction(image_path, save_dir = None, true_class = None, show_img = False):
    '''Given an image path, returns the predicted class and its probability'''
    classes = {'dirt': 0, 'marigold': 1, 'morning_glory': 2, 'pea': 3, 'radish': 4}
    image = load_img(image_path, target_size = (200, 200))
    x = np.reshape(img_to_array(image)/255.0, [1, 200, 200, 3])
    class_lookup = {v: k for k, v in classes.items()}
    prediction_index = model.predict_classes(x)[0]
    class_prob = round(model.predict(x)[0][prediction_index], 5)
    predicted_class = class_lookup[prediction_index]
    
    if show_img:
        title = f'Predicted class: {predicted_class}, prob = {class_prob} \n True Class: {true_class}'
        img = display_image(cv2.imread(image_path), title)
    
    if save_dir:
        image_name = image_path.split("\\")[len(image_path.split("\\")) - 1].split(".")[0]
        save_path = f'{save_dir}\\{image_name}_prediction.jpg'
        img.savefig(save_path, format = "png")
        
    return (predicted_class, class_prob, true_class)

predicted_class, class_prob, true_class = output_prediction(image_path = image)
print(f'predicted class: {predicted_class}')
print(f'probability: {class_prob}')