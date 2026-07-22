# 🎯 Face Attendance System

A modern **Face Recognition Attendance System** that automates attendance using facial recognition technology. The application provides a React-based frontend and a Python backend for face detection, recognition, image training, and attendance management.

---

## 📌 Overview

The Face Attendance System eliminates manual attendance by identifying registered users through facial recognition. It offers an intuitive interface for uploading images, training the recognition model, and tracking attendance efficiently.

---

## ✨ Features

- 🔐 Face Recognition Authentication
- 📸 Upload Student Images
- 🧠 Train Face Recognition Model
- ✅ Automatic Attendance Marking
- 👨‍🎓 Student Management
- 📂 Attendance Records
- ⚡ Fast Recognition
- 🎨 Modern Responsive UI
- 🔄 Real-time Backend Integration

---

## 🛠 Tech Stack

### Frontend
- React.js
- Vite
- Tailwind CSS
- JavaScript

### Backend
- Python
- OpenCV
- Face Recognition
- SQLite / SQL Database

---

## 📁 Project Structure

```text
FACE-ATTENDANCE-SYSTEM
│
├── backend
│   ├── attendance/
│   ├── trainer/
│   ├── uploads/
│   ├── database.py
│   ├── face_engine.py
│   ├── face_utils.py
│   ├── models.py
│   ├── train.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Anchalm4/smart-attendance-system.git
```

```bash
cd smart-attendance-system
```

---

# Backend Setup

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Backend

```bash
python main.py
```

---

# Frontend Setup

Navigate to frontend

```bash
cd frontend
```

Install packages

```bash
npm install
```

Run frontend

```bash
npm run dev
```

---

## 📸 Working Flow

1. Register student images.
2. Upload face images.
3. Train the face recognition model.
4. Start attendance.
5. Camera detects faces.
6. Attendance is recorded automatically.
7. View attendance records.

---

## 📷 Screenshots

Add screenshots here.

Example:

- Login Page
- Dashboard
- Upload Face
- Camera Detection
- Attendance Table

---

## 🚀 Future Improvements

- 🎯 Live Face Detection
- 😊 Face Mask Detection
- 📊 Attendance Analytics Dashboard
- 📧 Email Notifications
- ☁️ Cloud Database
- 📱 Mobile Responsive Version
- 📄 Export Attendance to Excel/PDF

---

## 💡 Why This Project?

Manual attendance is time-consuming and prone to errors. This project leverages AI-powered facial recognition to automate attendance, making the process faster, more secure, and more reliable.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

## ⭐ Show Your Support

If you like this project, please give it a ⭐ on GitHub.

---

## 👩‍💻 Author

**Anchal Mishra**

🔗 GitHub: https://github.com/Anchalm4

💼 LinkedIn: *(Add your LinkedIn Profile URL)*

---

## 📄 License

This project is licensed under the MIT License.
