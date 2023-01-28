import cv2
import os
import copy
import numpy as np
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import requests, json
 
# weather api key
api_key = "88cd16a2bf4b36c85acaac28009e7dbf"
weather_base_url = "http://api.openweathermap.org/data/2.5/weather?"

BOX_COLOR = (255, 0, 0) # Red
TEXT_COLOR = (255, 255, 255) # White

def visualize_bbox(img, bbox, class_name, color=BOX_COLOR, thickness=2):
    img = copy.deepcopy(img)
    x_center, y_center, w, h = bbox
    height, width, colors = img.shape
    w *= width
    h *= height
    x_center *= width
    y_center *= height
    x_min = x_center - w/2
    y_min = y_center - h/2
    x_min, x_max, y_min, y_max = int(x_min), int(x_min + w), int(y_min), int(y_min + h)
   
    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color=color, thickness=thickness)
    
    ((text_width, text_height), _) = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)    
    cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), BOX_COLOR, -1)
    cv2.putText(
        img,
        text=class_name,
        org=(x_min, y_min - int(0.3 * text_height)),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.35, 
        color=TEXT_COLOR, 
        lineType=cv2.LINE_AA,
    )
    return img

def cropToBbox(img, bbox):
    x_center, y_center, w, h = bbox
    height, width, colors = img.shape
    w *= width
    h *= height
    x_center *= width
    y_center *= height
    x_min = x_center - w/2
    y_min = y_center - h/2
    x_min, x_max, y_min, y_max = int(x_min), int(x_min + w), int(y_min), int(y_min + h)
    crop_img = img[y_min:y_max, x_min:x_max]
    return crop_img

def get_colors(img):
    pass

def get_complexity(img):
    edges = cv2.Canny(img,50,150,apertureSize = 3)
    cv2.imshow("cropped", edges)
    cv2.waitKey(0)
    w, h = edges.shape
    return 7*np.sum(edges)/(w*h*255)

#return True if basically the same color
#otherwise return False
#assuming color in BGR
def colorCompare(c1, c2, tolerance=20):
    color1_rgb = sRGBColor(c1[2], c1[1], c1[0])
    color2_rgb = sRGBColor(c2[2], c2[1], c2[0])
    color1_lab = convert_color(color1_rgb, LabColor)
    color2_lab = convert_color(color2_rgb, LabColor)
    delta_e = delta_e_cie2000(color1_lab, color2_lab)
    return (delta_e < tolerance)

# Sum of the min & max of (a, b, c)
def hilo(a, b, c):
    if c < b: b, c = c, b
    if b < a: a, b = b, a
    if c < b: b, c = c, b
    return a + c

def complement(b, g, r):
    k = hilo(b, g, r)
    return tuple(k - u for u in (b, g, r))

#return True if colors go together
#otherwise return False
def areCompatible(c1, c2):
    return not colorCompare(complement(c1[0], c1[1], c1[2]), c2, 40)

def bgr_to_hsv(b, g, r):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return h, s, v

def isGloomy(color, tolerance=65):
    h,s,v = bgr_to_hsv(color)
    return (v < tolerance)

def isNeutral(color, tolerance=75):
    h,s,v = bgr_to_hsv(color)
    return (s < tolerance)

def isVibrant(color):
    return isBright(color) and (not isNeutral(color))

def isBright(color, tolerance=80):
    h,s,v = bgr_to_hsv(color)
    return (v >= tolerance)

def getAesthetic(colors):
    

def getWeather(city_name):
    complete_url = weather_base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404": #city is found
        y = x["main"]
        current_temperature = y["temp"] #in kelvin
        current_pressure = y["pressure"] #in hPa
        current_humidity = y["humidity"] #in percentage
        z = x["weather"]
        weather_description = z[0]["description"]
    else:
        print(" City Not Found ")

weatherIncompatibility = {
    "warm":[],
    "cold":[]
}

strongColors = [] #in RGB
# Color check: color compatibility
# Weather check:
# Overall synergy:
# 1 color = too simple
# 0 stong colors = too simple
# >3 "strong" colors = too many
# complexity of clothing (average complexity rating should be about 0.5)
# aesthetic (gloomy, bland, bright)

pwd = os.path.realpath(os.path.dirname(__file__))
testimg = cv2.imread(pwd + "/test_imgs/complex_shirt.jpg")
