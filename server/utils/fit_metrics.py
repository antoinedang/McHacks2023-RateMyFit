import cv2
from skimage.restoration import estimate_sigma

BOX_COLOR = (255, 0, 0) # Red
TEXT_COLOR = (255, 255, 255) # White

def visualize_bbox(img, bbox, class_name, color=BOX_COLOR, thickness=2):
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

def get_colors(img):
    cv2.imshow("out", img)
    cv2.waitKey(0)

def toEdges(img):
    return cv2.Canny(img,50,150,apertureSize = 3)

def get_complexity(img):
    from skimage.restoration import estimate_sigma

def estimate_noise(image_path):
    img = cv2.imread(image_path)
    return estimate_sigma(img, multichannel=True, average_sigmas=True)

#return True if basically the same color
#otherwise return False
def colorCompare(c1, c2):


#return True if complementary colors
#otherwise return False
def areComplementary(c1, c2):

def isGloomy():

def isNeutral():

def isBright():

def getAesthetic(colors):

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