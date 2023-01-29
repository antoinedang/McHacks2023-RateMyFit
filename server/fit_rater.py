from utils import fit_metrics
from ultralytics import YOLO

def rate_my_fit(filepath):
    img = cv.imread(filepath)
    pred = model(img)
    for results in pred:
        box = results.boxes
        print(box)
        print("\nprediction:" + str(list(box.xywh)))
        print("\nprediction:" + str(list(box.conf)))
        print("\nprediction:" + str(list(box.cls)))
        
    text = "Rating your fit..."
    return img, text

# Load a model
model = YOLO("runs/detect/train2/weights/best.pt")  # load a model