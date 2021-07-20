import os
import cv2
import math
import random
import numpy as np

import Main
import Preprocess
import PossibleChar


kNearest = cv2.ml.KNearest_create()

# constants for checkIfPossibleChar, this checks one possible char only (does not compare to another char)
MIN_PIXEL_WIDTH = 2
MIN_PIXEL_HEIGHT = 8

MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1.0

MIN_PIXEL_AREA = 80

# constants for comparing two chars
MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0

MAX_CHANGE_IN_AREA = 0.5

MAX_CHANGE_IN_WIDTH = 0.8
MAX_CHANGE_IN_HEIGHT = 0.2

MAX_ANGLE_BETWEEN_CHARS = 12.0

# other constants
MIN_NUMBER_OF_MATCHING_CHARS = 3

RESIZED_CHAR_IMAGE_WIDTH = 20
RESIZED_CHAR_IMAGE_HEIGHT = 30

MIN_CONTOUR_AREA = 100




# check whether it is a possible char based on physical attributes
def checkIfPossibleChar(possibleChar):
    if (possibleChar.intBoundingRectArea > MIN_PIXEL_AREA and
        possibleChar.intBoundingRectWidth > MIN_PIXEL_WIDTH and
        possibleChar.intBoundingRectHeight > MIN_PIXEL_HEIGHT and
        possibleChar.fltAspectRatio > MIN_ASPECT_RATIO and
        possibleChar.fltAspectRatio < MAX_ASPECT_RATIO):
        return True
    else:
        return False


def findListOfListsOfMatchingChars(listOfPossibleChars):
    listOfListsOfMatchingChars = []

    for possibleChar in listOfPossibleChars:                       
        listOfMatchingChars = findListOfMatchingChars(possibleChar, listOfPossibleChars)        

        listOfMatchingChars.append(possibleChar)             

        if len(listOfMatchingChars) < MIN_NUMBER_OF_MATCHING_CHARS: 
            continue                    
        
        # voila!! we have found a possible group that could form a plate
        listOfListsOfMatchingChars.append(listOfMatchingChars)     

        listOfPossibleCharsWithCurrentMatchesRemoved = []
        # delete to avoid duplicated lists
        listOfPossibleCharsWithCurrentMatchesRemoved = list(set(listOfPossibleChars) - set(listOfMatchingChars))

        # recursive call
        recursiveListOfListsOfMatchingChars = findListOfListsOfMatchingChars(listOfPossibleCharsWithCurrentMatchesRemoved)     

        # for each list of matching chars found by recursive cal, we'll add it to our original list of lists of matching chars  
        for recursiveListOfMatchingChars in recursiveListOfListsOfMatchingChars: 
            listOfListsOfMatchingChars.append(recursiveListOfMatchingChars)             

        break       

    return listOfListsOfMatchingChars


def findListOfMatchingChars(possibleChar, listOfChars):
    listOfMatchingChars = []   

    for possibleMatchingChar in listOfChars:             
        if possibleMatchingChar == possibleChar:    
            continue      

        # trying to find a matching char
        fltDistanceBetweenChars = distanceBetweenChars(possibleChar, possibleMatchingChar)

        fltAngleBetweenChars = angleBetweenChars(possibleChar, possibleMatchingChar)

        fltChangeInArea = float(abs(possibleMatchingChar.intBoundingRectArea - possibleChar.intBoundingRectArea)) / float(possibleChar.intBoundingRectArea)

        fltChangeInWidth = float(abs(possibleMatchingChar.intBoundingRectWidth - possibleChar.intBoundingRectWidth)) / float(possibleChar.intBoundingRectWidth)
        fltChangeInHeight = float(abs(possibleMatchingChar.intBoundingRectHeight - possibleChar.intBoundingRectHeight)) / float(possibleChar.intBoundingRectHeight)

        if (fltDistanceBetweenChars < (possibleChar.fltDiagonalSize * MAX_DIAG_SIZE_MULTIPLE_AWAY) and
            fltAngleBetweenChars < MAX_ANGLE_BETWEEN_CHARS and
            fltChangeInArea < MAX_CHANGE_IN_AREA and
            fltChangeInWidth < MAX_CHANGE_IN_WIDTH and
            fltChangeInHeight < MAX_CHANGE_IN_HEIGHT):
            listOfMatchingChars.append(possibleMatchingChar)        

    return listOfMatchingChars                  


def distanceBetweenChars(firstChar, secondChar):
    intX = abs(firstChar.intCenterX - secondChar.intCenterX)
    intY = abs(firstChar.intCenterY - secondChar.intCenterY)

    return math.sqrt((intX ** 2) + (intY ** 2))


def angleBetweenChars(firstChar, secondChar):
    fltAdj = float(abs(firstChar.intCenterX - secondChar.intCenterX))
    fltOpp = float(abs(firstChar.intCenterY - secondChar.intCenterY))

    if fltAdj != 0.0:                           
        fltAngleInRad = math.atan(fltOpp / fltAdj) 
    else:
        fltAngleInRad = 1.5708     # pi/2 -> tan = infinity                    

    return fltAngleInRad * (180.0 / math.pi)    


