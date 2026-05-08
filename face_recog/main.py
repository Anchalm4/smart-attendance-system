import cv2
import os
import numpy as np
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import winsound

# ==============================
# 📁 PATHS
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dataset_path = os.path.join(BASE_DIR, "dataset")
attendance_file = os.path.join(BASE_DIR, "attendance.xlsx")

# ==============================
# 📂 CREATE DATASET FOLDER
# ==============================
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

# ==============================
# 📊 CREATE EXCEL FILE
# ==============================
if not os.path.exists(attendance_file):

    df = pd.DataFrame(
        columns=[
            "Name",
            "Date",
            "Time",
            "Status",
            "Attendance %"
        ]
    )

    df.to_excel(attendance_file, index=False)

# ==============================
# 📸 FACE DETECTOR
# ==============================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# ==============================
# 🧠 TRAIN MODEL
# ==============================
faces = []
labels = []

label_map = {}

current_label = 0

for person in os.listdir(dataset_path):

    person_path = os.path.join(dataset_path, person)

    if not os.path.isdir(person_path):
        continue

    label_map[current_label] = person

    for img_name in os.listdir(person_path):

        img_path = os.path.join(person_path, img_name)

        img = cv2.imread(img_path)

        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        detected_faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5
        )

        for (x, y, w, h) in detected_faces:

            face = gray[y:y+h, x:x+w]

            face = cv2.resize(face, (200, 200))

            faces.append(face)

            labels.append(current_label)

    current_label += 1

# ==============================
# ⚠️ NO DATA
# ==============================
if len(faces) == 0:

    print("No face images found in dataset folder.")
    exit()

faces = np.array(faces)
labels = np.array(labels)

# ==============================
# 🤖 LBPH MODEL
# ==============================
model = cv2.face.LBPHFaceRecognizer_create()

model.train(faces, labels)

# ==============================
# 🌗 THEME
# ==============================
dark_mode = True

# ==============================
# 📈 MARK ATTENDANCE
# ==============================
def mark_attendance(name):

    now = datetime.now()

    date = now.strftime("%Y-%m-%d")

    time = now.strftime("%H:%M:%S")

    try:

        df = pd.read_excel(attendance_file)
        df["Attendance %"] = df["Attendance %"].astype(float)

    except:

        df = pd.DataFrame(
            columns=[
                "Name",
                "Date",
                "Time",
                "Status",
                "Attendance %"
            ]
        )

    already_marked = (
        (df["Name"] == name)
        &
        (df["Date"] == date)
    ).any()

    if not already_marked:

        new_row = pd.DataFrame([{
            "Name": name,
            "Date": date,
            "Time": time,
            "Status": "Present",
            "Attendance %": 0.0
        }])

        df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

        total_days = df["Date"].nunique()

        for student in df["Name"].unique():

            present_days = len(
                df[
                    df["Name"] == student
                ]["Date"].unique()
            )

            percentage = round(
                (present_days / total_days) * 100,
                2
            )

            df.loc[
                df["Name"] == student,
                "Attendance %"
            ] = percentage

        df.to_excel(attendance_file, index=False)

# ==============================
# 🕘 COLLEGE TIMING
# ==============================
def is_college_time():

    current_hour = datetime.now().hour

    return 9 <= current_hour < 18

# ==============================
# 🌗 TOGGLE THEME
# ==============================
def toggle_theme():

    global dark_mode

    dark_mode = not dark_mode

    if dark_mode:

        root.configure(bg="#020617")

        canvas.configure(bg="#020617")

        glow.configure(bg="#2563eb")

        card.configure(bg="#0f172a")

    else:

        root.configure(bg="#e5e7eb")

        canvas.configure(bg="#e5e7eb")

        glow.configure(bg="#60a5fa")

        card.configure(bg="#ffffff")

# ==============================
# 🎥 ATTENDANCE SYSTEM
# ==============================
def start_attendance():

    if not is_college_time():

        winsound.Beep(500, 500)

        messagebox.showwarning(
            "Attendance Closed",
            "Attendance available only\nbetween 9:00 AM and 6:00 PM"
        )

        return

    status_label.config(
        text="● Opening Camera...",
        fg="#38bdf8"
    )

    cap = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW
    )

    if not cap.isOpened():

        messagebox.showerror(
            "Camera Error",
            "Unable to open webcam."
        )

        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    marked_students = set()

    scan_y = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        detected_faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5
        )

        # ==============================
        # ✨ SCAN LINE
        # ==============================
        scan_y += 5

        if scan_y > 480:
            scan_y = 0

        cv2.line(
            frame,
            (0, scan_y),
            (640, scan_y),
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "AI Face Scanning...",
            (180, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        for (x, y, w, h) in detected_faces:

            face = gray[y:y+h, x:x+w]

            face = cv2.resize(face, (200, 200))

            label, confidence = model.predict(face)

            if confidence < 60:

                name = label_map[label]

                if name in marked_students:
                    continue

                marked_students.add(name)

                mark_attendance(name)

                winsound.Beep(1200, 400)

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x+w, y+h),
                    (0, 255, 0),
                    3
                )

                cv2.putText(
                    frame,
                    f"{name} Present",
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

                cv2.imshow(
                    "Smart Attendance Scanner",
                    frame
                )

                cv2.waitKey(800)

                status_label.config(
                    text=f"● {name} Present",
                    fg="#22c55e"
                )

                next_person = messagebox.askyesno(
                    "Attendance Marked",
                    f"{name} marked present ✅\n\nNext Person?"
                )

                if next_person:

                    status_label.config(
                        text="● Ready For Next Person",
                        fg="#38bdf8"
                    )

                    break

                else:

                    cap.release()

                    cv2.destroyAllWindows()

                    status_label.config(
                        text="● Attendance Completed",
                        fg="#22c55e"
                    )

                    return

            else:

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x+w, y+h),
                    (255, 0, 0),
                    2
                )

                cv2.putText(
                    frame,
                    "Unknown Face",
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

        cv2.imshow(
            "Smart Attendance Scanner",
            frame
        )

        key = cv2.waitKey(1)

        if key == 27:
            break

    cap.release()

    cv2.destroyAllWindows()

    status_label.config(
        text="● SYSTEM READY",
        fg="#facc15"
    )

# ==============================
# 🎨 GUI
# ==============================
root = tk.Tk()

root.title(
    "Smart College Attendance System"
)

# ✅ FULLSCREEN
root.state("zoomed")

root.configure(bg="#020617")

# ==============================
# ✨ CANVAS
# ==============================
canvas = tk.Canvas(
    root,
    bg="#020617",
    highlightthickness=0
)

canvas.pack(fill="both", expand=True)

# ==============================
# ✨ PARTICLES
# ==============================
particles = []

for i in range(40):

    x = np.random.randint(0, 1500)

    y = np.random.randint(0, 900)

    size = np.random.randint(2, 5)

    particle = canvas.create_oval(
        x,
        y,
        x + size,
        y + size,
        fill="#38bdf8",
        outline=""
    )

    particles.append((particle, size))

# ==============================
# ✨ PARTICLE ANIMATION
# ==============================
def animate_particles():

    for particle, size in particles:

        canvas.move(particle, 0, 1)

        coords = canvas.coords(particle)

        if coords[1] > 900:

            x = np.random.randint(0, 1500)

            canvas.coords(
                particle,
                x,
                0,
                x + size,
                size
            )

    root.after(50, animate_particles)

animate_particles()

# ==============================
# 🔵 GLOW FRAME
# ==============================
glow = tk.Frame(
    root,
    bg="#2563eb"
)

glow.place(
    relx=0.5,
    rely=0.5,
    anchor="center",
    width=560,
    height=720
)

# ==============================
# 🖤 MAIN CARD
# ==============================
card = tk.Frame(
    root,
    bg="#0f172a"
)

card.place(
    relx=0.5,
    rely=0.5,
    anchor="center",
    width=520,
    height=700
)

# ==============================
# 🎓 ICON
# ==============================
icon = tk.Label(
    card,
    text="🎓",
    font=("Segoe UI Emoji", 42),
    bg="#0f172a",
    fg="#38bdf8"
)

icon.pack(pady=(25, 10))

# ==============================
# ✨ TITLE
# ==============================
title = tk.Label(
    card,
    text="Smart Attendance",
    font=("Segoe UI", 30, "bold"),
    bg="#0f172a",
    fg="#38bdf8"
)

title.pack()

# ==============================
# 🧠 SUBTITLE
# ==============================
subtitle = tk.Label(
    card,
    text="AI Powered Face Recognition",
    font=("Segoe UI", 12),
    bg="#0f172a",
    fg="#94a3b8"
)

subtitle.pack(pady=(5, 25))

# ==============================
# ⏰ CLOCK
# ==============================
clock_frame = tk.Frame(
    card,
    bg="#111827"
)

clock_frame.pack(pady=10)

clock = tk.Label(
    clock_frame,
    font=("Consolas", 32, "bold"),
    bg="#111827",
    fg="#22c55e",
    padx=25,
    pady=12
)

clock.pack()

def update_time():

    current = datetime.now().strftime(
        "%H:%M:%S"
    )

    clock.config(text=current)

    root.after(1000, update_time)

update_time()

# ==============================
# 📡 STATUS
# ==============================
status_label = tk.Label(
    card,
    text="● SYSTEM READY",
    font=("Segoe UI", 13, "bold"),
    bg="#0f172a",
    fg="#facc15"
)

status_label.pack(pady=25)

# ==============================
# 🟢 START BUTTON
# ==============================
start_btn = tk.Button(
    card,
    text="▶ START ATTENDANCE",
    font=("Segoe UI", 15, "bold"),
    bg="#22c55e",
    fg="white",
    activebackground="#16a34a",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=30,
    height=2,
    command=start_attendance
)

start_btn.pack(pady=(10, 18))

# ==============================
# 🌗 THEME BUTTON
# ==============================
theme_btn = tk.Button(
    card,
    text="🌗 TOGGLE THEME",
    font=("Segoe UI", 13, "bold"),
    bg="#3b82f6",
    fg="white",
    activebackground="#2563eb",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=30,
    height=2,
    command=toggle_theme
)

theme_btn.pack(pady=10)

# ==============================
# 🔴 EXIT BUTTON
# ==============================
exit_btn = tk.Button(
    card,
    text="⛔ EXIT SYSTEM",
    font=("Segoe UI", 15, "bold"),
    bg="#ef4444",
    fg="white",
    activebackground="#dc2626",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=30,
    height=2,
    command=root.destroy
)

exit_btn.pack(pady=(15, 10))

# ==============================
# ✨ FOOTER
# ==============================
footer = tk.Label(
    card,
    text="Powered by OpenCV AI • Real-Time Recognition",
    font=("Segoe UI", 10),
    bg="#0f172a",
    fg="#94a3b8"
)

footer.pack(side="bottom", pady=18)

# ==============================
# 🚀 RUN APP
# ==============================
root.mainloop()










#  .\final_env\Scripts\activate  
# python face_recog\main.py    