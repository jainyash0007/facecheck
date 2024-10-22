import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
from PIL import ImageTk, Image


# Train Image
def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message,text_to_speech):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(haarcasecade_path)
    faces, Id = getImagesAndLables(trainimage_path)
    recognizer.train(faces, np.array(Id))
    recognizer.save(trainimagelabel_path)
    res = "Image Trained successfully"  # +",".join(str(f) for f in Id)
    message.configure(text=res)
    text_to_speech(res)


def getImagesAndLables(path):
    # imagePath = [os.path.join(path, f) for d in os.listdir(path) for f in d]
    newdir = [os.path.join(path, d) for d in os.listdir(path)]
    imagePath = [
        os.path.join(newdir[i], f)
        for i in range(len(newdir))
        for f in os.listdir(newdir[i])
    ]
    faces = []
    Ids = []
    for imagePath in imagePath:
        # Open the image and convert it to grayscale
        pilImage = Image.open(imagePath).convert("L")
        imageNp = np.array(pilImage, "uint8")

        # Extract the filename
        filename = os.path.split(imagePath)[-1]  # Get 'Jain ayush_65_1.jpg'

        # Split by underscore and extract the second part (the ID)
        try:
            Id = int(filename.split("_")[1].strip())  # Extract '65' as the ID
        except ValueError as e:
            print(f"Error extracting ID from filename: {filename} -> {e}")
            continue  # Skip this file if there's an error

        # Append the grayscale face and the ID
        faces.append(imageNp)
        Ids.append(Id)

    return faces, Ids