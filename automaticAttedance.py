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
        now = time.time()
        future = now + 20

        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
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
                    return  # Exit if the model can't be loaded

                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                attendance = pd.DataFrame(columns=["Enrollment", "Name"])

                detected_ids = set()  # Keep track of already detected IDs

                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)

                    for (x, y, w, h) in faces:
                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

                        if conf < 70:  # Adjust threshold as needed
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")

                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            if len(aa) > 0:
                                name = aa[0]
                            else:
                                name = "Unknown"
                            
                            # Only add the ID if it hasn't been detected yet
                            if Id not in detected_ids:
                                tt = f"{Id}-{name}"
                                print(tt)

                                attendance.loc[len(attendance)] = [Id, name]
                                detected_ids.add(Id)  # Mark the ID as detected

                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(im, str(tt), (x + h, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 4)
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 25, 255), 4)

                    if time.time() > future:
                        break

                    cv2.imshow("Filling Attendance...", im)
                    if cv2.waitKey(30) & 0xFF == 27:
                        break

                cam.release()
                cv2.destroyAllWindows()
                

                # Create necessary folders if they don't exist
                if not os.path.exists(attendance_path):
                    os.makedirs(attendance_path)
                path = os.path.join(attendance_path, sub)
                if not os.path.exists(path):
                    os.makedirs(path)

                # Save attendance
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")

                fileName = f"{path}/{sub}_{date}_{Hour}-{Minute}-{Second}.csv"
                attendance.to_csv(fileName, index=False)
                print(f"Attendance saved to {fileName}")

                # Notify user
                m = f"Attendance filled successfully for {sub}"
                Notifica.configure(
                    text=m,
                    bg="black",
                    fg="yellow",
                    width=33,
                    relief=RIDGE,
                    bd=5,
                    font=("times", 15, "bold"),
                )
                text_to_speech(m)
                Notifica.place(x=20, y=250)

                # Show the attendance in a new window
                showAttendance(fileName)

            except Exception as e:
                f = f"No Face found for attendance. Error: {str(e)}"
                print(f)
                text_to_speech(f)
                cv2.destroyAllWindows()

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
