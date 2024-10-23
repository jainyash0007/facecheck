import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time

# take Image of user
def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    if (l1 == "") and (l2 == ""):
        t = 'Please Enter your Enrollment Number and Name.'
        text_to_speech(t)
    elif l1 == '':
        t = 'Please Enter your Enrollment Number.'
        text_to_speech(t)
    elif l2 == "":
        t = 'Please Enter your Name.'
        text_to_speech(t)
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier(haarcasecade_path)
            Enrollment = l1
            Name = l2
            sampleNum = 0
            directory = Enrollment + "_" + Name
            path = os.path.join(trainimage_path, directory)
            os.mkdir(path)
            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum += 1
                    cv2.imwrite(
                        os.path.join(path, f"{Name}_{Enrollment}_{str(sampleNum)}.jpg"),
                        gray[y: y + h, x: x + w],
                    )
                    cv2.imshow("Frame", img)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                elif sampleNum > 100:
                    break
            cam.release()
            cv2.destroyAllWindows()

            # Check if the CSV file exists
            file_exists = os.path.isfile("StudentDetails/studentdetails.csv")

            # Write to CSV with headers if not present
            with open("StudentDetails/studentdetails.csv", "a+", newline='') as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                
                # Write header only if file doesn't exist
                if not file_exists:
                    writer.writerow(["Enrollment", "Name"])
                
                # Write the student details
                writer.writerow([Enrollment, Name])

            res = "Images Saved for ER No:" + Enrollment + " Name:" + Name
            message.configure(text=res)
            text_to_speech(res)

        except FileExistsError as F:
            F = "Student Data already exists"
            text_to_speech(F)
