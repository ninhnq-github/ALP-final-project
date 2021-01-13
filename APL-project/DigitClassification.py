import torch
import matplotlib.pyplot as plt
import numpy as np
import torchvision

from torch import nn, optim
from torchvision import datasets, transforms

import cv2;

def Classify(model, img):
    test = np.array([img])
    test  = torch.from_numpy(test)
    model.requires_grad = False
    output = model(test.unsqueeze(0).cuda())
    _, predicted = torch.max(output, 1)
    digit = int(predicted[0])
    model.requires_grad = True
    return digit

def PreProcess(img):
    img = cv2.GaussianBlur(img,(5,5),0)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    img = img.astype('float32')
    img /= 255.0
    img = cv2.resize(img,(30,30),interpolation = cv2.INTER_AREA)
    img = img[1:29,1:29]
    return img

def ScanInfo(model):
    idcode = 0
    for i in range(1,9):
        gray = cv2.imread('Image\\'+str(i)+'.jpg', 0)
        preimg = PreProcess(gray)
        d = Classify(model, preimg)
        if (d==-1): return
        idcode = idcode * 10 + d
    return idcode

def ScanfPoint(model):
    point = 0
    for i in range(9,13):
        gray = cv2.imread('Image\\'+str(i)+'.jpg', 0)
        preimg = PreProcess(gray)
        d = Classify(model, preimg)
        if (d==-1): return
        point = point * 10 + d
    return point/100.0

def shapeDetection(cnt, sd, image, ratio):
    M = cv2.moments(cnt)
    if (float(M["m00"])==0 or float(M["m00"])==0):  return "No Shape"
    cX = int((M["m10"] / M["m00"]) * ratio)
    cY = int((M["m01"] / M["m00"]) * ratio)
    shape = sd.detect(cnt)
    cnt = cnt.astype("float")
    cnt *= ratio
    cnt = cnt.astype("int")
    cv2.waitKey(0)
    return shape

from ShapeDetectors import ShapeDetector
import imutils

def CropRect(img):
    h, w = img.shape[:2]
    img = cv2.resize(img,(1000,int(1000/w*h)),interpolation = cv2.INTER_AREA)
    h, w = img.shape[:2]
    
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(img, (1, 1), 0)
    thresh = cv2.threshold(blurred, 0, 255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    #cv2.imshow("image",thresh)
    cv2.waitKey(0)

    cnt, h = cv2.findContours(thresh.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in cnt]
    max_index = np.argmax(areas)
    areas[max_index] = 0
    max_index = np.argmax(areas)
    cnt_biggest=cnt[max_index]

    x,y,w,h = cv2.boundingRect(cnt_biggest)
    crop= img[ y:h+y,x:w+x]
 
    named = "Image_R/1.jpg"
    #print(named)
    cv2.imwrite(named, crop)
    #cv2.imshow("snip",crop )

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def CropImg(img):
    h, w = img.shape[:2]
    img = cv2.resize(img,(400,int(400/w*h)),interpolation = cv2.INTER_AREA)
    h, w = img.shape[:2]
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (1, 1), 0)
    thresh = cv2.threshold(blurred, 150, 255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    #cv2.imshow("image",thresh)
    
    cnt, h = cv2.findContours(thresh.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    sd = ShapeDetector()
    
    def get_contour_precedence(contour, rows):
        origin = cv2.boundingRect(contour)
        return origin[1] + origin[0]*rows

    cnt.sort(key=lambda x:get_contour_precedence(x, img.shape[1]))
    countRightContour = 0

    for i in range(len(cnt)):
        area = cv2.contourArea(cnt[i])
        #print(area)
        if(area>500 and area<1000 and shapeDetection(cnt[i], sd, img, ratio=1)=='square'):
            #print(shapeDetection(cnt[i], sd, img, ratio=1))
            countRightContour+=1
            mask = np.zeros_like(img)
            x,y,w,h = cv2.boundingRect(cnt[i])
            crop= img[ y:h+y,x:w+x]
            named = "Image\\" + str(countRightContour)+ ".jpg"
            cv2.imwrite(named, crop)
            #cv2.imshow("snip",crop )
            if(cv2.waitKey(0))==27:break
        if (countRightContour==12): break

    cv2.destroyAllWindows()

NAME_MODEL = 'model_final.pt'

def ScanfImg(name):
    img = cv2.imread(name,0);
    CropRect(img)
    rect = cv2.imread("Image_R\\1.jpg");
    CropImg(rect)
    model =  torch.load(NAME_MODEL)
    model.eval()
    studentID = ScanInfo(model)
    point = ScanfPoint(model)
    return studentID, point


for i in range(4):
    imgname = 'TEST/IMG'+str(i+1)+'.jpg'
    print(imgname)
    ScanfImg(imgname)

#imgname = 'TEST/IMG1.jpg'
#    print(imgname)
#ScanfImg(imgname)

#file = open('TestResult.csv','a')
#for i in range(33):
#    imgname = 'TEST/IMG'+str(i+1)+'.jpg'
#    print(imgname)
#    studentID, point = ScanfImg(imgname)
#    file.write('%d, %d, %f\n'%(i+1,studentID, point))
#file.close()
