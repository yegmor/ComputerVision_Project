import cv2.cv2 as cv2
import cv2
import numpy as np
import os
import string
from random import randrange
import shutil
import random


def drawOnImage(originalImg, writePath):
    # print("shape of image is: ", originalImg.shape, "\n")
    image = originalImg.copy()
    height, width, channel = originalImg.shape
    
    color = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
    thickness = -1
    rnd = randrange(0, 2)

    if rnd == 0:
        radius = height //2
        center_x = randrange(width // 8, width)
        center_y = randrange (height // 8, height)
        cv2.circle(image, center=(center_x, center_y), radius=radius, color=color, thickness=thickness)
   
    elif rnd == 1:
        x1 = randrange(width // 8, width//2)
        y1 = randrange (height // 8, height//2)
        x2 = randrange(width // 2, width)
        y2 = randrange (height // 2, height)
        cv2.rectangle(image, (x1, y1), (x2,y2), color=color, thickness=thickness)                             
    
    cv2.imwrite(writePath , image) 


if (__name__ == "__main__"):
    # for n in ["0", "1"] : 
        # for sec in ['train/', '/']:
    n = '0'
    sec = 'train/'
    # folder = "../Dataset/" + sec + n
    # writeFolder = "../Dataset/" + sec + "cropped_" + n 
    
    readFolder = "../Dataset/" + sec + "cropped_" + n 
    writeFolder = "../Dataset/" + sec + "cropped_damaged_" + n 
    
    for filename in os.listdir(readFolder):
        readPath = os.path.join(readFolder, filename)
        originalImg  = cv2.imread(readPath)   
        writePath = os.path.join(writeFolder, filename)
        drawOnImage(originalImg, writePath)  


def firstData(): #first step
    root_dir = 'D:/University/Computer Vision/Project/Dataset/' # data root path
    classes_dir = ['0', '1', '2'] #total labels

    test_ratio = 0.2

    for cls in classes_dir:
        os.makedirs(root_dir +'train/' + cls)
        os.makedirs(root_dir +'test/' + cls)

        # Creating partitions of the data after shuffeling
        src = root_dir + "/" + cls # Folder to copy images from

        allFileNames = os.listdir(src)
        np.random.shuffle(allFileNames)

        
        train_FileNames, test_FileNames = np.split(
                                            np.array(allFileNames), [int(len(allFileNames) * (1 - test_ratio))]
                                            )

        train_FileNames = [src+'/'+ name for name in train_FileNames.tolist()]
        test_FileNames = [src+'/' + name for name in test_FileNames.tolist()]

        print('Total images: ', len(allFileNames))
        print('Training: ', len(train_FileNames))
        print('Testing: ', len(test_FileNames))

        # Copy-pasting images
        for name in train_FileNames:
            shutil.copy(name, root_dir +'train/' + cls)

        for name in test_FileNames:
            shutil.copy(name, root_dir +'test/' + cls)

         
def moveData():
    root_dir = 'D:/University/Computer Vision/Project/Dataset/' # data root path

    test_ratio = 0.2

    # for sec in ['train/', 'test/']:

    src = root_dir + 'cropped_damaged_0' # Folder to copy images from

    allFileNames = os.listdir(src)
    np.random.shuffle(allFileNames)

    train_FileNames, test_FileNames = np.split(np.array(allFileNames), [int(len(allFileNames) * (1 - test_ratio))])

    train_FileNames = [src + '/' + name for name in train_FileNames.tolist()]
    test_FileNames = [src + '/' +  name for name in test_FileNames.tolist()]

    print('Total images: ', len(allFileNames))
    print('Training: ', len(train_FileNames))
    print('Testing: ', len(test_FileNames))

    # Copy-pasting images
    for name in train_FileNames:
        shutil.copy(name, root_dir + 'train')

    for name in test_FileNames:
        shutil.copy(name, root_dir + 'test')