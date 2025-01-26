import tkinter as tk
from tkinter import filedialog, messagebox
import student

STUDENT_LIST = []
FILE_PATH = ''

def upload_file():
    global FILE_PATH
    FILE_PATH = filedialog.askopenfilename()
    if FILE_PATH:
        label_file.config(text=f"File selected: {FILE_PATH}")

# Create the main application 
root = tk.Tk()
root.title("Simple GUI Example")
root.geometry("400x300")  # Width x Height

# Create a label to display the selected file
label_file = tk.Label(root, text="No file selected", wraplength=300)
label_file.pack(pady=10)

button_upload = tk.Button(root, text="Upload File", command=upload_file)
button_upload.pack(pady=10)

label = tk.Label(root, text="Enter Number of Students")
label.pack(pady=5)

# Create a button to upload a file
# Create a text entry box
entry_box = tk.Entry(root, width=30)
entry_box.pack(pady=5)

# Create a button to retrieve the input
button = tk.Button(root, text="Generate", command=lambda: student.generate_students(int(entry_box.get()), STUDENT_LIST))
button.pack(pady=10)

button = tk.Button(root, text="Start", command=lambda:  student.detect_students(STUDENT_LIST, FILE_PATH))
button.pack(pady=20)

# Run the main application loop
root.mainloop()
