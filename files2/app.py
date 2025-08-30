import cv2
import time
import sqlite3
from flask import Flask, render_template, Response, jsonify
from detection.yolo_weapon import detect_weapons, detect_crowd
from detection.face_recognition import detect_faces
from detection.pose_hand import detect_pose_hand, detect_fall
from detection.emotion import detect_emotion
from detection.tracking import detect_intrusion_loitering
from notification.sms import send_sms_alert
from notification.email import send_email_alert
from utils.health import system_health_check
from utils.attendance import process_attendance

app = Flask(__name__)
events = []

# Database setup (simplified)
def log_event_to_db(event):
    conn = sqlite3.connect('database/events.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (timestamp REAL, type TEXT, message TEXT)''')
    c.execute("INSERT INTO events VALUES (?, ?, ?)", (event['timestamp'], event['type'], event['message']))
    conn.commit()
    conn.close()

def process_events(frame):
    detected_events = []
    # Each detection module returns a list of events (can be empty)
    detected_events += detect_weapons(frame)
    detected_events += detect_crowd(frame)
    detected_events += detect_faces(frame)
    detected_events += detect_pose_hand(frame)
    detected_events += detect_fall(frame)
    detected_events += detect_emotion(frame)
    detected_events += detect_intrusion_loitering(frame)
    detected_events += process_attendance(frame)
    # System health events (optional)
    detected_events += system_health_check()
    # Handle new events
    for event in detected_events:
        if not events or events[-1]['message'] != event['message']:
            events.append(event)
            log_event_to_db(event)
            # Notify if critical
            if event['type'] in ['weapon', 'fight', 'intrusion', 'fall', 'blacklist', 'distress', 'crowd']:
                send_sms_alert(event['message'])
                send_email_alert(event['message'])
    return detected_events

def gen_frames():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise RuntimeError("Could not open webcam.")
    while True:
        success, frame = cam.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)
        process_events(frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/events')
def get_events():
    return jsonify(events[-10:])  # last 10 events

if __name__ == '__main__':
    app.run(debug=True)