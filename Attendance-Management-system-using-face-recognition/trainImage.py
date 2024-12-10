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
    faces = []
    ids = []

    # Loop through all subdirectories and files in the given path
    for root, dirs, files in os.walk(path):
        for file in files:
            # Only process image files (jpg, png, etc.)
            if file.endswith('.jpg') or file.endswith('.png'):
                imagePath = os.path.join(root, file)

                # Open the image and convert to grayscale
                pilImage = Image.open(imagePath).convert("L")
                imageNp = np.array(pilImage, "uint8")

                # Extract the filename
                filename = os.path.split(imagePath)[-1]

                # Split by underscore and extract the second part (the ID)
                try:
                    Id = int(filename.split("_")[1].strip())  # Extract '65' as the ID
                except (IndexError, ValueError) as e:
                    print(f"Error extracting ID from filename: {filename} -> {e}")
                    continue  # Skip files that do not follow the naming convention

                # Append the grayscale face and the ID
                faces.append(imageNp)
                ids.append(Id)

    return faces, ids

def retrain_model(trainimage_path, trainimagelabel_path, haarcasecade_path):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(haarcasecade_path)

    faces, ids = getImagesAndLables(trainimage_path)
    recognizer.train(faces, np.array(ids))
    recognizer.save(trainimagelabel_path)
    print("Model retrained successfully!")