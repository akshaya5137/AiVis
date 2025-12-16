# AiVis – Smart Face Recognition Attendance System
### *Your Face, Your Key*

![AiVis Dashboard]
<img width="1377" height="915" alt="image" src="https://github.com/user-attachments/assets/7532214b-501e-407c-884b-11aa4d140848" />


## 📋 Overview
**AiVis** is a modern, dark-themed Face Recognition Attendance System built with **Python**, **OpenCV**, and **Tkinter**. It allows you to register users via webcam, train a recognition model, and mark attendance in real-time with a "Neo-Tech" dashboard interface.
This project was developed as a **Python mini project**, focusing on practical applications of machine learning, OpenCV, and GUI development.

---

## Project Structure

AiVis/
│
├── dataset/                       # Stored face images (ID.Name format)
│   ├── 1.Akshaya/
│   ├── 2.Ananya/
│   └── ...
│
├── trainer/                       # Trained recognition model and mappings
│   ├── trainer.yml
│   └── names.json
│
├── attendance/                    # Attendance session records
│   └── attendance_session.csv
│
├── __pycache__/                   # Python cache files
│
├── main.py                        # GUI and application logic
├── backend.py                     # Face recognition and core functionality
├── requirements.txt               # Project dependencies
└── README.md                      # Project documentation

---
## ✨ Features
*   **Neo-Tech Dark UI**: A sleek, high-contrast dashboard with a "Minimal Dark Neo-Tech" aesthetic built with Tkinter.
*   **Real-Time Recognition**: Uses OpenCV's Local Binary Patterns Histograms (LBPH) for accurate face detection and recognition.
*   **Session-Based Attendance**: Automatically resets attendance on new sessions (configurable).
*   **User Management**: Register, View, Rename, and Delete users directly from the GUI.
*   **Live Reporting**: See "Present" vs "Absent" status with pill-style badges in real-time.
*   **Consolidated Codebase**: Optimized into just 2 main files for easy maintenance.

## 🛠️ Tech Stack
*   **Language**: Python 3.10+
*   **Computer Vision**: OpenCV (`opencv-contrib-python`)
*   **UI Framework**: Tkinter (`ttk` themed widgets)
*   **Data Processing**: Numpy, CSV

## 🚀 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/aivis.git
    cd aivis
    ```

2.  **Install Dependencies**
    ```bash
    pip install opencv-contrib-python numpy
    ```

## 💻 Usage

1.  **Run the Application**
    ```bash
    python aivis.py
    ```

2.  **Workflow**
    *   **Step 1: Register User** - Click "Register User", enter an ID and Name, and look at the camera to capture 100 sample images.
    *   **Step 2: Train Model** - Click "Train Model" to generate the recognition file (`trainer.yml`). **Must do this after every new registration or deletion.**
    *   **Step 3: Start Camera** - The system will now recognize faces and mark them as "Present" in the report.
    *   **Step 4: Live Session Report** - Displays present and absent users dynamically during the session.
    *   **Step 4: Manage Users** - Allows renaming or deleting registered users and retraining the model if required.


## 📂 Project Structure
```
AiVis/
├── aivis.py            # Main GUI Application (Entry Point)
├── backend.py          # Core Logic (Face Capture, Training, Database)
├── requirements.txt    # Dependencies
├── dataset/            # Stores user face images (ID.Name folder format)
├── trainer/            # Stores trained model (trainer.yml) and names (names.json)
└── attendance/         # Stores session CSV logs
```

### Prerequisites
- Python 3.9 or later
- Webcam


## 📸 Screenshots
*   **Homepage**:
    <img width="1377" height="915" alt="image" src="https://github.com/user-attachments/assets/5a3fc1d1-f983-45b3-bb6e-78c567c6448c" />

*   **Manage Users**:
    <img width="1377" height="915" alt="image" src="https://github.com/user-attachments/assets/f1729cd1-b41f-43d8-9394-e7a4cc862bbe" />

*   **Start Camera**:
    <img width="1369" height="907" alt="image" src="https://github.com/user-attachments/assets/81aab092-dc3c-4368-818d-3dfaaa492496" />



### Clone the Repository
```bash
git clone https://github.com/your-username/AiVis.git
cd AiVis


## 📜 License
This project is open-source and available under the MIT License.

