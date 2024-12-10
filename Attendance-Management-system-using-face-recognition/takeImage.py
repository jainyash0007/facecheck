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
        return
    elif l1 == '':
        t = 'Please Enter your Enrollment Number.'
        text_to_speech(t)
        return
    elif l2 == "":
        t = 'Please Enter your Name.'
        text_to_speech(t)
        return

    # Paths and setup
    student_details_file = "StudentDetails/studentdetails.csv"
    os.makedirs(os.path.dirname(student_details_file), exist_ok=True)  # Ensure directory exists

    # Ensure the CSV file exists and has correct headers
    if not os.path.exists(student_details_file):
        with open(student_details_file, "w", newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(["Enrollment", "Name"])  # Write headers

    # Load student details for duplicate checks
    try:
        student_data = pd.read_csv(student_details_file)
        if "Enrollment" not in student_data.columns or "Name" not in student_data.columns:
            raise ValueError("Student details file is corrupted or missing headers.")
    except Exception as e:
        t = f"Error loading student details: {str(e)}"
        text_to_speech(t)
        message.configure(text=t)
        return

    # Check if the Enrollment No already exists
    if l1 in student_data["Enrollment"].astype(str).values:
        t = f"Student with Enrollment No: {l1} is already registered."
        text_to_speech(t)
        message.configure(text=t)
        return

    # Check if the face is already registered
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read("TrainingImage/Trainner.yml")  # Load the trained model
    except Exception:
        t = "No trained model found. Please train the model first."
        text_to_speech(t)
        message.configure(text=t)
        return

    # Start camera and detect faces
    detector = cv2.CascadeClassifier(haarcasecade_path)
    cam = cv2.VideoCapture(0)  # Initialize the camera once
    sampleNum = 0
    detected_duplicate = False
    directory = f"{l1}_{l2}"
    path = os.path.join(trainimage_path, directory)
    os.makedirs(path, exist_ok=True)  # Ensure directory exists

    while True:
        ret, img = cam.read()
        if not ret:
            t = "Failed to capture image from the camera."
            text_to_speech(t)
            message.configure(text=t)
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]

            # Predict the face to check for duplicates
            id, confidence = recognizer.predict(face)
            if confidence < 70:  # Adjust the threshold as necessary
                matched_row = student_data.loc[student_data["Enrollment"] == str(id)]
                if not matched_row.empty:
                    t = (f"Face already registered with Enrollment No: {id}. "
                         f"Cannot register again.")
                    text_to_speech(t)
                    message.configure(text=t)
                    detected_duplicate = True
                    break

            # If no duplicate detected, save the image
            sampleNum += 1
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imwrite(
                os.path.join(path, f"{l2}_{l1}_{str(sampleNum)}.jpg"),
                gray[y: y + h, x: x + w],
            )
            cv2.putText(img, f"Capturing: {sampleNum}/100", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        if detected_duplicate or sampleNum >= 100:
            break

        cv2.imshow("Capturing Images...", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()

    if detected_duplicate:
        return

    # Write the student details to the CSV file
    with open(student_details_file, "a", newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([l1, l2])

    res = f"Images Saved for Enrollment No: {l1}, Name: {l2}"
    message.configure(text=res)
    text_to_speech(res)
