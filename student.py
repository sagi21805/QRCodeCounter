import os
from datetime import datetime, timedelta
import qr
import cv2
from pyzbar import pyzbar

class Student:
    
    def __init__(self, id, path):
        self.identifier = str(id)
        self.reps = 0
        self.recognized = False
        self.last_detected = datetime.fromtimestamp(0)
        qr.generate(self.identifier).save(f'{path}/{id}.jpg')
    

def generate_students(number_of_students) -> list[Student]:
    base_path = f'Students QRcodes {datetime.date(datetime.now())}'
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    return [Student(i, base_path) for i in range(number_of_students)]

def detect_students(student_list: list[Student]):

    # Initialize camera
    cap = cv2.VideoCapture(0)  # 0 for default camera

    print("Starting live multi-QR code detection. Press 'q' to quit.")

    frame_count = 0
    
    while True:
        
        ret, frame = cap.read()
        frame_count += 1
        if frame_count % 3 != 0:
            continue
        # Capture frame-by-frame
        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        # Decode QR codes in the frame
        decoded_objects = pyzbar.decode(frame)

        for obj in decoded_objects:
            
            if obj.type != 'QRCODE':
                continue
            
            qr_data = int(obj.data.decode("utf-8"))
            detection_time = datetime.now()
            if (detection_time - student_list[qr_data].last_detected) > timedelta(seconds=1):
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
