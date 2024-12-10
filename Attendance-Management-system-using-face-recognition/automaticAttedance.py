import tkinter as tk
from tkinter import *
import os, cv2
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time

# Paths for necessary files and folders
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImage\\Trainner.yml"
trainimage_path = "TrainingImage"
studentdetail_path = "StudentDetails\\studentdetails.csv"
attendance_path = "AttendanceSystem"

# Function for choosing the subject and filling attendance
def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
            return

        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            try:
                recognizer.read(trainimagelabel_path)
            except Exception as e:
                e = "Model not found, please train the model."
                Notifica.configure(
                    text=e,
                    bg="black",
                    fg="yellow",
                    width=33,
                    font=("times", 15, "bold"),
                )
                Notifica.place(x=20, y=250)
                text_to_speech(e)
                return

            face_cascade = cv2.CascadeClassifier(haarcasecade_path)
            df = pd.read_csv(studentdetail_path)

            # Initialize attendance tracker
            detected_ids = set()  # Set to keep track of marked IDs
            attendance = pd.DataFrame(columns=["Enrollment", "Name"])  # Attendance DataFrame

            # Initialize webcam
            cam = cv2.VideoCapture(0)
            now = time.time()
            future = now + 20  # Time limit for the attendance loop

            while True:
                ret, im = cam.read()
                if not ret:
                    break

                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

                for (x, y, w, h) in faces:
                    id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                    if confidence < 70:  # Face recognized
                        name = df.loc[df["Enrollment"] == id, "Name"].values
                        name = name[0] if len(name) > 0 else "Unknown"

                        # If the student is not already marked present
                        if id not in detected_ids:
                            detected_ids.add(id)
                            attendance.loc[len(attendance)] = [id, name]  # Add to attendance
                            t = f"Marked Present: {id} - {name}"
                            print(t)
                            text_to_speech(t)

                        # Draw rectangle and display ID
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(im, f"{id}-{name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    else:  # Face not recognized
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        cv2.putText(im, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                if time.time() > future:
                    break

                cv2.imshow("Filling Attendance...", im)
                if cv2.waitKey(30) & 0xFF == 27:  # Exit on pressing ESC
                    break

            cam.release()
            cv2.destroyAllWindows()

            # Save attendance to file
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H-%M-%S")
            path = os.path.join(attendance_path, sub)

            if not os.path.exists(path):
                os.makedirs(path)

            attendance_file = f"{path}/{sub}_{date}_{timeStamp}.csv"
            attendance.to_csv(attendance_file, index=False)

            t = f"Attendance saved to {attendance_file}"
            text_to_speech(t)
            print(t)

            # Display the attendance in a new window
            showAttendance(attendance_file)

        except Exception as e:
            t = f"Error: {str(e)}"
            text_to_speech(t)
            print(t)

    def showAttendance(fileName):
        root = Tk()
        root.title(f"Attendance of {tx.get()}")
        root.configure(background="black")

        with open(fileName, newline="") as file:
            reader = csv.reader(file)
            r = 0
            for col in reader:
                c = 0
                for row in col:
                    label = Label(
                        root,
                        width=10,
                        height=1,
                        fg="yellow",
                        font=("times", 15, "bold"),
                        bg="black",
                        text=row,
                        relief=tk.RIDGE,
                    )
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        root.mainloop()

    ### Window setup for subject chooser
    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)

    titl = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=160, y=12)

    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="yellow",
        fg="black",
        width=33,
        height=2,
        font=("times", 15, "bold"),
    )

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(f"AttendanceSystem\\{sub}")

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)

    subject.mainloop()
