import os
from datetime import datetime, timedelta
import qr
import cv2
from pyzbar import pyzbar
from tkinter import messagebox
import os 

class Student:
    
    def __init__(self, id):
        self.identifier = str(id)
        self.reps = 0
        self.recognized = False
        self.last_detected = datetime.fromtimestamp(0)
    

def generate_students(number_of_students, student_list):
    """
    This funtion takes the number of students and generates
    qrcodes for each students, the given list is set to the created list 
    """
    base_path = f'Students QRcodes {datetime.date(datetime.now())}'
    qr.generate_qr_pdf(number_of_students, f"{base_path}.pdf")
    student_list[:] = [Student(i) for i in range(number_of_students)]
    messagebox.showinfo("Information", f"qrcodes are generated at {os.path.abspath(f'{base_path}.pdf')}")
        

def detect_students(student_list: list[Student], video_path):

    if not student_list and not video_path:
        messagebox.showinfo("Information", "Please enter number of students and choose a file!")
        return
    if not video_path:
        messagebox.showinfo("Information", "Please choose a file!")
    if not student_list:
        messagebox.showinfo("Information", "Please enter number of students and generate codes")
        return    

    # Initialize camera
    cap = cv2.VideoCapture(video_path)  # 0 for default camera

    print("Starting live multi-QR code detection. Press 'q' to quit.")
    
    while True:
        
        ret, frame = cap.read()

        # frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        # Capture frame-by-frame
        if not ret:
            print("Failed to grab frame. Exiting...")
            with open('result.txt', 'w') as f:
                f.write(f"Studemt {qr_data} has done {student_list[qr_data].reps} reps")
                f.close()
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 5)

        # Decode QR codes in the frame
        decoded_objects = pyzbar.decode(frame)

        for obj in decoded_objects:
            
            if obj.type != 'QRCODE':
                continue
            
            qr_data = int(obj.data.decode("utf-8"))
            detection_time = datetime.now()
            if (detection_time - student_list[qr_data].last_detected) > timedelta(seconds=0.2):
                student_list[qr_data].reps += 1 
                print(f"Student {qr_data} has done {student_list[qr_data].reps} reps")                
            
            student_list[qr_data].last_detected = detection_time
            # Annotate the frame
            cv2.putText(
                frame,
                str(qr_data),
                (obj.rect.left, obj.rect.top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

        # Display the resulting frame
        cv2.imshow("Multi QR Code Detector", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
