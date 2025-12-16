import cv2, os, json, numpy as np, csv, shutil, time
from datetime import datetime

# --- HELPER ---
def get_users(folders_only=False):
    """Returns {ID: Name} or {ID: FolderName} based on param."""
    if not os.path.exists("dataset"): return {}
    users = {}
    for f in [d for d in os.listdir("dataset") if os.path.isdir(os.path.join("dataset", d))]:
        try:
            parts = f.split('.', 1)
            users[parts[0]] = parts[1] if not folders_only else f
        except: continue
    return users

# --- CORE LOGIC ---
def capture_faces(uid, name):
    if not uid or not name: return
    path = os.path.join("dataset", f"{uid}.{name}")
    os.makedirs(path, exist_ok=True)
    
    cam = cv2.VideoCapture(0)
    if not cam.isOpened(): return
    face_cls = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    count = 0
    
    while count < 100:
        ret, frame = cam.read()
        if not ret: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for (x, y, w, h) in face_cls.detectMultiScale(gray, 1.3, 5):
            cv2.imwrite(os.path.join(path, f"{count}.jpg"), gray[y:y+h, x:x+w])
            count += 1
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{count}/100", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            time.sleep(0.05)
        cv2.imshow("Registering", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cam.release(); cv2.destroyAllWindows()

def train_model():
    os.makedirs("trainer", exist_ok=True)
    if not os.path.exists("dataset"): return
    faces, ids, names = [], [], {}

    for uid, name in get_users().items():
        names[uid] = name
        path = os.path.join("dataset", f"{uid}.{name}")
        for img in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
            im_data = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
            if im_data is not None: faces.append(im_data); ids.append(int(uid))

    if faces:
        rec = cv2.face.LBPHFaceRecognizer_create()
        rec.train(faces, np.array(ids))
        rec.save("trainer/trainer.yml")
        with open("trainer/names.json", 'w') as f: json.dump(names, f)

def start_attendance():
    if not os.path.exists("trainer/trainer.yml"): return
    rec = cv2.face.LBPHFaceRecognizer_create(); rec.read("trainer/trainer.yml")
    with open("trainer/names.json", 'r') as f: names = json.load(f)
    
    cam = cv2.VideoCapture(0); cls = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    while True:
        ret, frame = cam.read()
        if not ret: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for (x, y, w, h) in cls.detectMultiScale(gray, 1.2, 5):
            idn, conf = rec.predict(gray[y:y+h, x:x+w])
            name = names.get(str(idn), "Unknown") if conf < 100 else "Unknown"
            if conf < 55: mark_attendance_csv(str(idn), name)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.imshow('Attendance', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cam.release(); cv2.destroyAllWindows()

def mark_attendance_csv(uid, name):
    os.makedirs("attendance", exist_ok=True)
    fpath = "attendance/attendance_session.csv"
    if not os.path.exists(fpath):
        with open(fpath, 'w', newline='') as f: csv.writer(f).writerow(["ID", "Name", "Date", "Time"])
    
    with open(fpath, 'r') as f:
        if any(row and row[0] == str(uid) for row in csv.reader(f)): return

    with open(fpath, 'a', newline='') as f:
        csv.writer(f).writerow([uid, name, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])

def get_attendance_data():
    present = set()
    if os.path.exists("attendance/attendance_session.csv"):
        with open("attendance/attendance_session.csv", 'r') as f:
            present = {row[0] for row in csv.reader(f) if row and row[0].isdigit()}
    
    registered = get_users()
    p_list = [(uid, name) for uid, name in registered.items() if uid in present]
    a_list = [(uid, name) for uid, name in registered.items() if uid not in present]
    return p_list, a_list, datetime.now().strftime("%Y-%m-%d")

def manage_user(uid, action, new_name=None):
    users = get_users(folders_only=True)
    if uid not in users: return False, "Not Found"
    try:
        if action == "delete":
            shutil.rmtree(os.path.join("dataset", users[uid]))
            return True, "Deleted"
        elif action == "rename" and new_name:
            os.rename(os.path.join("dataset", users[uid]), os.path.join("dataset", f"{uid}.{new_name}"))
            return True, "Renamed"
    except Exception as e: return False, str(e)
    return False, "Error"

def view_registered_users():
    if not os.path.exists("dataset"): return
    for u in [d for d in os.listdir("dataset") if os.path.isdir(os.path.join("dataset", d))]:
        imgs = os.listdir(os.path.join("dataset", u))
        if imgs:
            im = cv2.imread(os.path.join("dataset", u, imgs[0]))
            if im is not None:
                im = cv2.resize(im, (300, 300))
                cv2.putText(im, u, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow(f"User: {u}", im); cv2.moveWindow(f"User: {u}", 100, 100); cv2.waitKey(0); cv2.destroyAllWindows()
