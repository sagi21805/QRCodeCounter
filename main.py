import student
import qr

def main():
    list = student.generate_students(10)
    student.detect_students(list)
    print("---------------------------")
    for s in list:
        print(f"Student: {s.identifier} has done: {s.reps} reps")
    print("---------------------------")


if __name__ == '__main__':
    main()