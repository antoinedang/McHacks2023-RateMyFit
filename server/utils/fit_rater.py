from utils import fit_metrics
from ultralytics import YOLO
import cv2
import json
import utils.fit_metrics as utils
import os
def get_fit_ratings_from_metrics(img):
    """
    Returns a json file of metrics and their ratings
    """
    
    
    assigned_ratings = {"color complementary": utils.get_colors(img),
            "mood/aesthetic": utils.getAesthetic(img),
            "geometric complexity": utils.get_complexity(img),
            "weather compatibility": utils.getWeather("Montreal"),
            }
    #Concatenate to string
    str_ratings = ', '.join(key + value for key, value in assigned_ratings.items())
    return str_ratings
    

    
    
def rate_my_fit(filepath):
    img = cv2.imread(filepath)
    #get rating from image
    get_fit_ratings_from_metrics(img)
    return img, "test \n new line"
    pred = model(img)
    for results in pred:
        box = results.boxes
        print(box)
        print("\nprediction:" + str(list(box.xywh)))
        print("\nprediction:" + str(list(box.conf)))
        print("\nprediction:" + str(list(box.cls)))
    #delete filepath
    os.remove(filepath)
    text = "Rating your fit..."
    return img, text

# Load a model
#model = YOLO("runs/detect/train2/weights/best.pt")  # load a model