import cv2
import numpy as np
import math
import Main


GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9


def getGrayThreshImg(imgOriginal):
    height, width, numChannels = imgOriginal.shape

    imgHSV = np.zeros((height, width, 3), np.uint8)
    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)
    imgHue, imgSaturation, imgGrayscale = cv2.split(imgHSV)

    #increase contrast
    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    
    imgTopHat = np.zeros((height, width, 1), np.uint8)
    imgBlackHat = np.zeros((height, width, 1), np.uint8)

    imgTopHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_TOPHAT, structuringElement)
    imgBlackHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_BLACKHAT, structuringElement)

    imgGrayscalePlusTopHat = cv2.add(imgGrayscale, imgTopHat)
    imgMaxContrastGray = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

    imgBlurred = np.zeros((height, width, 1), np.uint8)
    imgBlurred = cv2.GaussianBlur(imgMaxContrastGray, GAUSSIAN_SMOOTH_FILTER_SIZE, 0)

    imgThresh = cv2.adaptiveThreshold(imgBlurred, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)

    # # kernel = np.ones((5, 5), np.uint8)
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    # # kernel2 = np.ones((7, 7), np.uint8)
    # kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5, 5))
    # # kernel3 = np.ones((3, 3), np.uint8)
    # kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3, 3))
    # # kernel4 = np.ones((3, 3), np.uint8)
    # kernel4 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3, 3))

    # sobelx =np.abs(cv2.Sobel(imgThresh, cv2.CV_64F, 1, 0, ksize=5))
    # sobely = cv2.Sobel(sobelx, cv2.CV_64F, 0, 1, ksize=5)

    # abs_img = np.absolute(sobely)
    # _,threshold_img =  cv2.threshold(abs_img,170,255,cv2.THRESH_BINARY)
    # cv2.imshow("threshold_img!", threshold_img)
    # open1_img = cv2.morphologyEx(threshold_img, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("open1_img!", open1_img)
    # close_img = cv2.morphologyEx(open1_img, cv2.MORPH_CLOSE, kernel2)
    # cv2.imshow("close_img!", close_img)
    # erode_img = cv2.erode(close_img, kernel3, iterations=1)
    # cv2.imshow("erode_img!", erode_img)
    # dilate_img = cv2.dilate(erode_img, kernel4, iterations=1)
    # cv2.imshow("dilate_img!", dilate_img)

    # # sobely = cv2.Sobel(imgThresh, cv2.CV_64F, 0, 1, ksize=5)
    # # cv2.imshow("sobelY!", sobely)
    # cv2.imshow("dilate_img!", dilate_img)
    
    # open sefid mohat bar siah omit
    # close siah mohat bar sefid omit
    # openStructElmntCircle = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(8, 8))
    # openedImg1 = cv2.morphologyEx(imgThresh, cv2.cv2.MORPH_OPEN, openStructElmntCircle)
    # cv2.imshow("first openedImg", openedImg1)

    # closeStructElmntCircle = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2, 2))
    # closedImg1 = cv2.morphologyEx(openedImg1, cv2.cv2.MORPH_CLOSE, closeStructElmntCircle)
    # cv2.imshow("then closedImg", closedImg1)


    # closeStructElmntCircle = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2, 2))
    # closedImg2 = cv2.morphologyEx(imgThresh, cv2.cv2.MORPH_CLOSE, closeStructElmntCircle)
    # cv2.imshow("first closedImg", closedImg2)

    # openStructElmntCircle = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(8, 8))
    # openedImg2 = cv2.morphologyEx(closedImg2, cv2.cv2.MORPH_OPEN, openStructElmntCircle)
    # cv2.imshow("then openedImg", openedImg2)
    
    return imgGrayscale, imgThresh


# !!!!belongs to main.py
def CropPlate(imgOriginalScene, mainPlate, path):
    # get 4 vertices of rotated rect
    p2fRectPoints = cv2.boxPoints(mainPlate.rrLocationOfPlateInScene)          
    
    minY, maxY, minX, maxX = 1000000, 0, 10000000, 0
    for point in p2fRectPoints:
        x = point[0]
        y = point[1]

        if x < minX: minX = x
        if x > maxX: maxX = x
        if y < minY: minY = y
        if y > maxY: maxY = y
    if minX < 0: minX = 0
    if minY < 0: minY = 0
    
    # draw lines around recognized plate
    # cv2.line(imgOriginalScene, tuple((minX, minY)), tuple((maxX, minY)), YELLOW, 2)        
    # cv2.line(imgOriginalScene, tuple((maxX, minY)), tuple((maxX, maxY)), YELLOW, 2)
    # cv2.line(imgOriginalScene, tuple((maxX, maxY)), tuple((minX, maxY)), YELLOW, 2)
    # cv2.line(imgOriginalScene, tuple((minX, maxY)), tuple((minX, minY)), YELLOW, 2)
    
    # cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), RED, 2)         
    # cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), RED, 2)
    # cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), RED, 2)
    # cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), RED, 2)
    
    croppedImg = imgOriginalScene[int(minY): int(maxY), int(minX): int(maxX)]
    
    if Main.showSteps == True: 
        cv2.imshow("original", imgOriginalScene)
        cv2.imshow("cropped", croppedImg)

    # cv2.imwrite(path, croppedImg)
    
    return croppedImg
