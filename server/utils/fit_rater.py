from utils import fit_metrics
from ultralytics import YOLO
import cv2
import utils.fit_metrics
import os

def rate_my_fit(filepath):
    img = cv2.imread(filepath)
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