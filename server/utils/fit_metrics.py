from cv2 import imshow, waitKey, rectangle, putText, getTextSize, FONT_HERSHEY_SIMPLEX, LINE_AA, Canny
import os
import copy
import numpy as np
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import requests, json
from sklearn.cluster import KMeans
 
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
   
    rectangle(img, (x_min, y_min), (x_max, y_max), color=color, thickness=thickness)
    
    ((text_width, text_height), _) = getTextSize(class_name, FONT_HERSHEY_SIMPLEX, 0.35, 1)    
    rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), BOX_COLOR, -1)
    putText(
        img,
        text=class_name,
        org=(x_min, y_min - int(0.3 * text_height)),
        fontFace=FONT_HERSHEY_SIMPLEX,
        fontScale=0.35, 
        color=TEXT_COLOR, 
        lineType=LINE_AA,
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
    flat_img = np.reshape(img,(-1,3))
    kmeans = KMeans(n_clusters=5,random_state=0)
    kmeans.fit(flat_img)
    dominant_colors = np.array(kmeans.cluster_centers_,dtype='uint')
    percentages = (np.unique(kmeans.labels_,return_counts=True)[1])/flat_img.shape[0]
    p_and_c = zip(percentages,dominant_colors)
    colors = []
    for p,c in p_and_c:
        if p > 0.1:
            colors.append(c)
    return colors

def get_complexity(img):
    edges = Canny(img,50,150,apertureSize = 3)
    #imshow("cropped", edges)
    #waitKey(0)
    w, h = edges.shape
    return 7*np.sum(edges)/(w*h*255)

#return True if basically the same color
#otherwise return False
#assuming color in BGR
def areTheSame(c1, c2, tolerance=20):
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

#return True if colors go together (will say that colors that don't go together are any two of RGB)
#otherwise return False
def areCompatible(c1, c2):
    if areTheSame((255, 0, 0), c1, 40):
        if areTheSame((255, 0, 0), c2, 40): return True
        elif areTheSame((0, 255, 0), c2, 40): return False
        elif areTheSame((0, 0, 255), c2, 40): return False
    elif areTheSame((0, 255, 0), c1, 40):
        if areTheSame((255, 0, 0), c2, 40): return False
        elif areTheSame((0, 255, 0), c2, 40): return True
        elif areTheSame((0, 0, 255), c2, 40): return False
    elif areTheSame((0, 0, 255), c1, 40):
        if areTheSame((255, 0, 0), c2, 40): return False
        elif areTheSame((0, 255, 0), c2, 40): return False
        elif areTheSame((0, 0, 255), c2, 40): return True
    return True

def bgr_to_hsv(c):
    b, g, r = c
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

def getAesthetic(colors, tolerance=0.5):
    aesthetics = [0, 0] #vibrant or gloomy
    for c in colors:
        if isVibrant(c): aesthetics[0] += 1
        elif isGloomy(c): aesthetics[1] += 1
    aesthetics[0] *= 1/len(colors)
    aesthetics[1] *= 1/len(colors)
    if aesthetics[0] > tolerance: return "vibrant"
    elif aesthetics[1] > tolerance: return "gloomy"
    else: return "neutral"

def getWeather(city_name):
    complete_url = weather_base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404": #city is found
        y = x["main"]
        current_temperature = y["temp"] #in kelvin
        z = x["weather"]
        weather_description = z[0]["description"]
        return current_temperature-273.15, weather_description
    else:
        print(" City Not Found ")
        return 15, "boring"


# describe what we see
# complexity of clothing (average complexity rating should be about 0.5)
# 0 stong colors = too simple
# >3 "strong" colors = too many
# Color check: color compatibility
# Weather check



# aesthetic (gloomy, bland, bright)