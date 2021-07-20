# DetectPlates.py

import cv2
import numpy as np
import math
import Main
import random

import Preprocess
import DetectChars
import PossiblePlate
import PossibleChar


PLATE_WIDTH_PADDING_FACTOR = 1.3
PLATE_HEIGHT_PADDING_FACTOR = 1.5


def detectPlatesInScene(imgOriginalScene):
    possiblePlatesList = []            

    height, width, numChannels = imgOriginalScene.shape

    imgGrayscaleScene = np.zeros((height, width, 1), np.uint8)
    imgThreshScene = np.zeros((height, width, 1), np.uint8)
    imgContours = np.zeros((height, width, 3), np.uint8)

    cv2.destroyAllWindows()

    if Main.showSteps == True: 
        cv2.imshow("0", imgOriginalScene)
    
    imgGrayscaleScene, imgThreshScene = Preprocess.getGrayThreshImg(imgOriginalScene)       
    
    if Main.showSteps == True:
        cv2.imshow("1a", imgGrayscaleScene)
        cv2.imshow("1b", imgThreshScene)

    # all possible chars in the scene: finds all contours and only returns contours that could be chars (solely comparison of each char)
    listOfPossibleCharsInScene = findPossibleCharsInScene(imgThreshScene)

    if Main.showSteps == True: 
        print("step 2 - len(listOfPossibleCharsInScene) = " + str(len(listOfPossibleCharsInScene)))

        imgContours = np.zeros((height, width, 3), np.uint8)
        contours = []
        for possibleChar in listOfPossibleCharsInScene:
            contours.append(possibleChar.contour)

        cv2.drawContours(imgContours, contours, -1, Main.WHITE)
        cv2.imshow("2b", imgContours)

    # with a list of all possible chars, find groups of matching chars
    listOfListsOfMatchingCharsInScene = DetectChars.findListOfListsOfMatchingChars(listOfPossibleCharsInScene)

    if Main.showSteps == True:
        print("step 3 - listOfListsOfMatchingCharsInScene.Count = " + str(len(listOfListsOfMatchingCharsInScene))) 

        imgContours = np.zeros((height, width, 3), np.uint8)

        for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
            contours = []

            for matchingChar in listOfMatchingChars:
                contours.append(matchingChar.contour)
            cv2.drawContours(imgContours, contours, -1, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        cv2.imshow("3", imgContours)

    # each group of matching chars could be announced as a plate
    for listOfMatchingChars in listOfListsOfMatchingCharsInScene:                   
        possiblePlate = extractPlate(imgOriginalScene, listOfMatchingChars)        

        # if any plate? -> welcome to possible plates list
        if possiblePlate.imgPlate is not None:                         
            possiblePlatesList.append(possiblePlate)                  

    if Main.showSteps == True: 
        # print("\n" + str(len(possiblePlatesList)) + " possible plates found")  
        print("\n")
        cv2.imshow("4a", imgContours)

        for i in range(0, len(possiblePlatesList)):
            p2fRectPoints = cv2.boxPoints(possiblePlatesList[i].rrLocationOfPlateInScene)

            cv2.line(imgContours, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), Main.RED, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), Main.RED, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), Main.RED, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), Main.RED, 2)

            cv2.imshow("4a", imgContours)

            print("possible plate " + str(i) + ", click on any image and press a key to continue . . .")

            cv2.imshow("4b", possiblePlatesList[i].imgPlate)
            cv2.waitKey(0)
        print("\nplate detection complete, click on any image and press a key to begin char recognition . . .\n")
        cv2.waitKey(0)

    return possiblePlatesList


def findPossibleCharsInScene(imgThresh):
    listOfPossibleChars = []               
    imgThreshCopy = imgThresh.copy()
    height, width = imgThresh.shape
    imgContours = np.zeros((height, width, 3), np.uint8)

    contours, _ = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  

    for i in range(0, len(contours)):  
        if Main.showSteps == True:                    
            cv2.drawContours(imgContours, contours, i, Main.WHITE)

        possibleChar = PossibleChar.PossibleChar(contours[i])
        if DetectChars.checkIfPossibleChar(possibleChar):                 
            listOfPossibleChars.append(possibleChar)           

    if Main.showSteps == True: 
        print("\nstep 2 - len(contours) = " + str(len(contours))) 
        cv2.imshow("2a", imgContours)

    return listOfPossibleChars


def extractPlate(imgOriginal, listOfMatchingChars):
    possiblePlate = PossiblePlate.PossiblePlate()      

    # sort chars from left to right (based on x position)
    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)        

    # calculate the center point of the plate by means of leftmost and rightmost point
    fltPlateCenterX = (listOfMatchingChars[0].intCenterX + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterX) / 2.0
    fltPlateCenterY = (listOfMatchingChars[0].intCenterY + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY) / 2.0
    ptPlateCenter = fltPlateCenterX, fltPlateCenterY

    # calculate plate width and height
    intPlateWidth = int(
        (listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectX +
            listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectWidth - 
            listOfMatchingChars[0].intBoundingRectX)
     * PLATE_WIDTH_PADDING_FACTOR)

    intTotalOfCharHeights = 0

    # sum of height hame chars -> yahtamel for affine
    for matchingChar in listOfMatchingChars:
        intTotalOfCharHeights = intTotalOfCharHeights + matchingChar.intBoundingRectHeight
    fltAverageCharHeight = intTotalOfCharHeights / len(listOfMatchingChars)

    intPlateHeight = int(fltAverageCharHeight * PLATE_HEIGHT_PADDING_FACTOR)

    # calculate correction angle of plate region
    fltOpposite = listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY - listOfMatchingChars[0].intCenterY
    # vatar mosalas qaem alzavie = distance shoon
    fltHypotenuse = DetectChars.distanceBetweenChars(listOfMatchingChars[0], listOfMatchingChars[len(listOfMatchingChars) - 1])
    
    fltCorrectionAngleInRad = math.asin(fltOpposite / fltHypotenuse)
    fltCorrectionAngleInDeg = fltCorrectionAngleInRad * (180.0 / math.pi)


    # calculated everything about this possible plate so compress all infos
    possiblePlate.rrLocationOfPlateInScene = ( tuple(ptPlateCenter), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg )

    # let's perform the actual rotation
    # get the rotation matrix for our calculated correction angle
    rotationMatrix = cv2.getRotationMatrix2D(tuple(ptPlateCenter), fltCorrectionAngleInDeg, 1.0)
    height, width, numChannels = imgOriginal.shape     

    imgRotated = cv2.warpAffine(imgOriginal, rotationMatrix, (width, height))       

    imgCropped = cv2.getRectSubPix(imgRotated, (intPlateWidth, intPlateHeight), tuple(ptPlateCenter))

    possiblePlate.imgPlate = imgCropped         # copy the cropped plate image into the applicable member variable of the possible plate

    return possiblePlate
