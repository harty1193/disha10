from picamera2 import Picamera2
from time import sleep
import cv2
import openai
import numpy as np
from pyzbar import pyzbar
from PIL import Image
def detect_circle(file):
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    start_x = 0
    start_y = 0
    side = 0
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.3, 400)
    if circles is not None:
        circles = np.round(circles[0,:]).astype("int")
        print(circles)
        for (x, y,r) in circles:
            cv2.circle(gray, (x,y),r, (0,255,0),2)
            start_x = x-r-5
            start_y = y-r-5
            side = 2*r+20
            if start_x >0 and start_y >0:
                crop_img = gray[start_y:start_y+side, start_x:start_x+side]
                #cv2.imshow("circle", crop_img)
                cv2.imwrite("circle.jpeg", crop_img)
                decode_qrcode()
        return True
    return False
def decode_qrcode():
    img = Image.open("circle.jpeg")
    qrcode = pyzbar.decode(img)
    if qrcode:
        data = qrcode[0].data.decode("utf-8")
        print(data)
        if data:
            ask_ai(data)
            return data
    return "Inside QR"
def ask_ai(ans):
    text = "As a car driver, I am at junction where I can either take right or left turn and their is signaltelling" + ans +"Give me single word answer, which direction should I turn"
    response = openai.ChatCompletion.create(engine="test1",
            messages = [{"role":"user", "content":text}],
            temperature=0.7,
            max_tokens = 800,
            top_p = 0.5,
            stop=None)
    print(response)
    return "Inside AI"

picam2 = Picamera2()
openai.api_type = "azure"
openai.api_base = "https://testingsogar.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = "2c8b723d594f42da9834e3942cf0c7e2"
file_name = "pic"
picam2.start()
for i in range(10):
    file_path = "/home/sogar/images/"+file_name+ str(i)+".jpg"
    print(file_path)
    sleep(2)
    picam2.capture_file(file_path)
    detect_circle(file_path)
        # stop bot
        #ans = decode_qrcode()
        #if ans:
        #    ask_ai(ans)
picam2.stop()
