import os
import cv2
import string
import numpy as np

import DetectPlates
import DetectChars
import PossiblePlate


BLACK = (0.0, 0.0, 0.0)
WHITE = (255.0, 255.0, 255.0)
YELLOW = (0.0, 255.0, 255.0)
GREEN = (0.0, 255.0, 0.0)
RED = (0.0, 0.0, 255.0)

showSteps = False


def main(path, writePath):
    imgOriginalScene  = cv2.imread(path)
    if imgOriginalScene is None:                           
        print("\nerror: image not read from file \n\n")  
        # pause so user can see error message
        os.system("pause")                                 
        return                                             

    possiblePlatesList = DetectPlates.detectPlatesInScene(imgOriginalScene)        
    
    plateCount = len(possiblePlatesList)
    

    if showSteps == True: 
        cv2.imshow("imgOriginalScene", imgOriginalScene)          

    # no plates found
    if len(possiblePlatesList) == 0:        
        # print("\nno license plates were detected\n")  
        return 'False', plateCount
        
    # at leat one possible plate found   
    else:
        # sort DESCENDING 
        possiblePlatesList.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

        # most recognized chars (suppose it's actual plate)
        mainPlate = possiblePlatesList[0]

        if len(mainPlate.strChars) == 0:                 
            # print("\nno characters were detected\n\n") 
            return 'True', plateCount                                       
        
        # croppedImgChars = CropPlate(imgOriginalScene, mainPlate, writePath)       
        
        if showSteps == True: 
            # cv2.imshow("ourCroppedImg", croppedImgChars) 
            cv2.imshow("otherCroppedImg", mainPlate.imgPlate)          
            cv2.imshow("imgThresh", mainPlate.imgThresh)

            # write license plate text in terminal
            # print("\nlicense plate read from image = " + mainPlate.strChars + "\n")
            # write license plate text on the image
            # writeLicensePlateCharsOnImage(imgOriginalScene, mainPlate)           

        # cv2.imwrite("imgOriginalScene.png", imgOriginalScene)
                 
        # print("----------------------------------------")
        cv2.waitKey(0)					
        
        return 'True', plateCount
    return 



if __name__ == "__main__":
    # attempt KNN training

    result = []
    accuracy = []
    total_num = 0
    total_true = 0
    for n in ["0","1", "2"] : 
        # for sec in ['train/', 'test/']:
        # readFolder = "../Dataset/" + sec + n 
        # writeFolder = "../Dataset/" + sec + n 
        readFolder = "../Dataset/"+ n 
        writeFolder = "../Dataset/" + n 
        num_true = 0
        count = 0
        
        for filename in os.listdir(readFolder):
            count += 1
            path = os.path.join(readFolder, filename)
            writePath = os.path.join(writeFolder, filename)
            
            isAnyPlate,  plateCount = main(path, writePath)

            if isAnyPlate == 'True': predClass = '0'
            elif isAnyPlate == 'False': predClass = '2'
            elif  plateCount >= 2 : predClass = '1'
            
            if n == predClass : num_true += 1
            #path , plate(0, 1) | non plate (2)
            r = path + ", " + predClass
            #  + str(plateChars.translate(str.maketrans('', '', string.whitespace))
            
            if showSteps == True: 
                print(r)

            result.append(r)
        
        total_num += count
        total_true += num_true
        acu = readFolder + " accuracy :" + str(num_true/count) + ", total :" + str(count) 
        print(acu)
        accuracy.append(acu)

    accuracy.append("total accuracy :" + str(total_true/total_num) + ", total :" + str(total_num))
    resultPath = "../Dataset/predictions.txt"
    with open(resultPath, "w") as file_: 
        # Writing data to a file 
        for a in accuracy:
            file_.write(a) 
            file_.writelines("\n") 
        for r in result:
            file_.write(r) 
            file_.writelines("\n") 
