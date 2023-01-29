from utils import fit_metrics
from ultralytics import YOLO
from cv2 import imread
import json
import utils.fit_metrics as metrics
import os
import numpy as np
from torch import tensor
from scipy.spatial import KDTree
from webcolors import hex_to_rgb
from webcolors import CSS3_HEX_TO_NAMES

def convert_bgr_to_name(bgr_tuple):
    rgb_tuple = (bgr_tuple[2], bgr_tuple[1], bgr_tuple[0])
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return str(names[index])

def generateRating(img, outfit, city):
    """
    Returns a string describing the rating of a particular outfit
    """
    temp, weather_description = metrics.getWeather(city)
    supercold=False
    cold=False
    warm=False
    hot=False
    if temp < 0: supercold=True
    elif temp > 30: hot=True
    elif temp > 21: warm=True
    elif temp < 10: cold=True
    main_colors = []
    strong_colors = []
    complexities = []
    aesthetics = {"neutral":0, "gloomy":0, "vibrant":0}
    incompatibilities = []
    for category, bbox in outfit:
        cropped_article = metrics.cropToBbox(img, bbox)
        complexities.append(metrics.get_complexity(cropped_article))
        colors = metrics.get_colors(cropped_article)
        main_colors.append((category, colors[0]))
        for c in colors:
            if not metrics.isNeutral(c):
                add = True
                for strongC in strong_colors:
                    if metrics.areTheSame(strongC, c): add = False
                if add: strong_colors.append(c)
        aesthetics[metrics.getAesthetic(colors)] += 1
        if supercold and category in weatherIncompatibility["supercold"]: incompatibilities.append(category)
        elif cold and category in weatherIncompatibility["cold"]: incompatibilities.append(category)
        elif warm and category in weatherIncompatibility["warm"]: incompatibilities.append(category)
        elif hot and category in weatherIncompatibility["hot"]: incompatibilities.append(category)

    out = "After careful analysis of your fit, I came to the following conclusions:XYou've got on "
    if len(main_colors) > 1:
        out += "a"
        for category, color in main_colors[:-1]:
            out += " " + convert_bgr_to_name(color) + " " + category + ", a"
        out += "nd a " + convert_bgr_to_name(main_colors[-1][1]) + " " + main_colors[-1][0] + ".X"
    elif len(main_colors) == 1:
        out += "a " + convert_bgr_to_name(main_colors[0][1]) + " " + main_colors[0][0] + ".X"
    else: 
        out += "nothing discernible. Dress up and try again."
        return out
    out += " The overall complexity of the patterns in your outfit were scored at " + str(np.mean(complexities)*100) + " percent, "
    if np.mean(complexities) > 0.7: out += "a bit high for my liking... Maybe throw in some solid colors?X"
    elif np.mean(complexities) < 0.3: out += "which is pretty low... Try spicing it up with some fun patterns next time.X"
    else: "a very reasonable score. Keep up the good work.X"

    out += "In terms of your color palette, "
    if len(strong_colors) > 3: out += "I noticed that you've opted for not one, not two, but " + str(len(strong_colors)) + " bold colors for your fit. While I commend your creativity, you should consider throwing in some muted tones as well...X"
    elif len(strong_colors) == 0: out += "I couldn't help but notice you've only chosen neutral colors today. A splash of color would do you wonders!X"
    
    errors = []
    for _, c1 in main_colors:
        for _, c2 in main_colors:
            if not metrics.areCompatible(c1, c2): 
                errors.append((convert_bgr_to_name(c1), convert_bgr_to_name(c2)))
    out += "When it comes to color theory, you made " + str(len(errors)) + " mistakes. "
    if len(errors) > 0:
        out += "Those were the following color pairs: " + str(errors) + "... Maybe take some notes for next time.X"
    else:
        out += "Congrats!X"

    out += "Now, let's check how this all fares for the outdoors. The temperature in " + city + " right now is about " + str(temp) + " Celsius (" + weather_description + ").X"


    if len(incompatibilities) > 1:
        for inc in incompatibilities[:-1]:
            out += "Maybe you should re-think wearing the " + str(inc) + ", "
        out += "and " + incompatibilities[-1] + ".X"
    elif len(incompatibilities) == 1:
        out += "Maybe you should re-think wearing the " + str(incompatibilities[0]) + "...X"
    else:
        out += "I think your fit will do just fine.X"
    
    gloomCount = 100*aesthetics["gloomy"]/len(outfit)
    vibCount = 100*aesthetics["vibrant"]/len(outfit)
    neutralCount = 100*aesthetics["neutral"]/len(outfit)

    out += "Anyway, I've scored your vibe as " + str(gloomCount) + " percent gloomy, " + str(vibCount) + " percent bubbly, and " + str(neutralCount) + " percent boring.XKeep up the good work!"
    
    return out
    
def rate_my_fit(filepath, city):
    img = imread(filepath)
    if have_a_model:
        pred = model(img)
        outfit = []
        for results in pred:
            box = results.boxes.numpy()
            for b in box:
                bbox = list(b.xywh[0])
                h, w, channels = img.shape
                bbox[0] *= 1/w
                bbox[1] *= 1/h
                bbox[2] *= 1/w
                bbox[3] *= 1/h
                class_name = names[int(list(b.cls)[0])]
                if float(list(b.conf)[0]) > 0.65:
                    outfit.append((class_name, bbox))
    else:
        outfit = [
            ("hat", [0.4640625, 0.0625, 0.13203125, 0.11171875]),
            ("short-sleeve shirt", [0.45, 0.31875, 0.2921875, 0.29453125]),
            ("pair of pants", [0.4671875, 0.67109375, 0.225, 0.45546875]),
            ("shoe", [0.5421875, 0.93203125, 0.0671875, 0.07421875]),
            ("shoe", [0.4109375, 0.93359375, 0.13125, 0.0984375])
        ]

    text = generateRating(img, outfit, city)
    for class_name, bbox in outfit:
        img = metrics.visualize_bbox(img, bbox, class_name)
    #delete filepath
    os.remove(filepath)
    return img, text

weatherIncompatibility = {
    "hot":["long-sleeve shirt", "long-sleeveoutwear", "pair of pants"],
    "warm":["long-sleeveoutwear"],
    "cold":["short-sleeve shirt", "pair of shorts", "skirt"],
    "supercold":["short-sleeve shirt", "short-sleeveoutwear", "pair of shorts", "skirt"]
}

pwd = os.path.realpath(os.path.dirname(__file__))
names = ["short-sleeve shirt", "long-sleeve shirt", "short-sleeveoutwear", "long-sleeveoutwear", "pair of shorts", "pair of pants", "skirt", "hat", "shoe"]
# Load a model
model = YOLO(pwd + "/best.pt")  # load a model
have_a_model = True