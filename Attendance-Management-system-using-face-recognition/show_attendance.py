import pandas as pd
from glob import glob
import os
import tkinter as tk
import csv
import tkinter as tk
from tkinter import *

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return

        # Call the attendance aggregation function here
        aggregate_attendance(Subject)

        # After aggregation, display the attendance in a new window
        root = tk.Tk()
        root.title(f"Attendance of {Subject}")
        root.configure(background="black")
        aggregated_file = f"AttendanceSystem\\{Subject}\\{Subject}_aggregated_attendance.csv"
        
        if not os.path.exists(aggregated_file):
            t = f"No attendance data found for {Subject}."
            text_to_speech(t)
            return
        
        with open(aggregated_file) as file:
            reader = csv.reader(file)
            r = 0

            for col in reader:
                c = 0
                for row in col:
                    label = tk.Label(
                        root,
                        width=15,
                        height=1,
                        fg="yellow",
                        font=("times", 15, " bold "),
                        bg="black",
                        text=row,
                        relief=tk.RIDGE,
                    )
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        root.mainloop()

    def aggregate_attendance(subject):
        # Path to the attendance folder for the given subject
        attendance_path = f"AttendanceSystem\\{subject}"
        
        # Check if the aggregated file exists, and remove it before starting a new aggregation
        aggregated_file = f"{attendance_path}\\{subject}_aggregated_attendance.csv"
        if os.path.exists(aggregated_file):
            os.remove(aggregated_file)  # Delete the old aggregated file
        
        if not os.path.exists(attendance_path):
            print(f"No attendance records found for the subject: {subject}")
            return

        # Find all CSV files for the subject
        attendance_files = glob(f"{attendance_path}\\{subject}_*.csv")
        if not attendance_files:
            print(f"No attendance files found for the subject: {subject}")
            return
        
        # Initialize an empty dataframe to store aggregated attendance
        all_attendance = pd.DataFrame()

        # Loop through each attendance file and merge the data
        for file in attendance_files:
            if "aggregated" in file:  # Skip any previously aggregated files if they exist
                continue
            df = pd.read_csv(file)
            
            # Extract only the date and time from the filename for the session name
            session_name = os.path.basename(file).replace(f"{subject}_", "").replace(".csv", "")
        
            # Each file represents attendance for one session; create a new column for that session
            df[session_name] = 1  # Mark all present students with 1 for this session
            
            if all_attendance.empty:
                all_attendance = df
            else:
                # Merge with the previous attendance records (outer join to include all students)
                all_attendance = pd.merge(all_attendance, df, on=['Enrollment', 'Name'], how='outer')

        # Replace NaN with 0, which means absent for that session
        all_attendance.fillna(0, inplace=True)

        # Calculate the Percentage for each student
        session_columns = all_attendance.columns[2:]  # Columns after 'Enrollment' and 'Name' are sessions
        all_attendance['Sessions Attended'] = all_attendance[session_columns].sum(axis=1)
        total_sessions = len(session_columns)
        all_attendance['Percentage'] = (all_attendance['Sessions Attended'] / total_sessions * 100).round(2)
        
        # Output the final attendance report
        all_attendance.to_csv(aggregated_file, index=False)
        
        print(f"Aggregated attendance report saved to {aggregated_file}")
        print(all_attendance[['Enrollment', 'Name', 'Percentage']])

    # Tkinter GUI setup
    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)

    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

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
        text="View Attendance",
        command=calculate_attendance,
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
