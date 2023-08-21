print("------ Importing Yolo ------")
from ultralytics import YOLO
print("------ Importing pytesseract and cv2 ------")
import pytesseract, cv2
print("------ Importing model ------" )
model = YOLO('best.pt')
print("------ Imported Model ------")
import numpy as np

def detect_number(image, offset=0):
    if not isinstance(image, np.ndarray):
        raise Exception("image input must be of type numpy.ndarray (use cv2.imread-return-object)")
    
    results = model(image, verbose=False)
    try: 
        boxes = results[0].boxes.cpu().numpy()
        r = boxes[0].xyxy[0].astype(int)
    except Exception as e:
        print("No number detected")
        return None, None

    img_crop = image.copy()[(r[1]-offset):(r[3]+offset), (r[0]-offset):(r[2]+offset)]
    img_rect = cv2.rectangle(image.copy(), (r[0], r[1]), (r[2], r[3]), (255, 255, 0), 4)

    return img_crop, img_rect

def extract_number(image, psm=13):
    confi = "-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm {}".format(psm)
    number = pytesseract.image_to_string(image, config=confi).strip()
    number = number.strip()
    number = number.replace(" ", "")
    if(len(number)==4 and number[0].isalpha() and number[1:].isnumeric()):
        return number
    else:
        return None

"""
print("Loaded")
img = cv2.imread("2.jpg")
results = model(img)

boxes = results[0].boxes.cpu().numpy()
r = boxes[0].xyxy[0].astype(int)
img_crop = img[r[1]:r[3], r[0]:r[2]]

cv2.imshow("Test", img_crop)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(pytesseract.image_to_string(img_crop))
"""