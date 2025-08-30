from ultralytics import YOLO
import time

# Load YOLO model (replace with your custom weights if available)
model = YOLO('yolov8n.pt')  # Use your weapon/fight weights if available

WEAPON_CLASSES = {"knife", "gun"}
FIGHT_CLASSES = {"fight", "person fighting"}

def detect_weapons(frame):
    detected_events = []
    results = model(frame)
    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            name = result.names[cls].lower()
            if name in WEAPON_CLASSES:
                detected_events.append({
                    'timestamp': time.time(),
                    'type': 'weapon',
                    'message': f'Weapon Detected: {name.capitalize()}'
                })
            if name in FIGHT_CLASSES:
                detected_events.append({
                    'timestamp': time.time(),
                    'type': 'fight',
                    'message': f'Fight Detected'
                })
    return detected_events

def detect_crowd(frame, threshold=10):
    detected_events = []
    results = model(frame)
    count = 0
    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            name = result.names[cls].lower()
            if name == 'person':
                count += 1
    if count >= threshold:
        detected_events.append({
            'timestamp': time.time(),
            'type': 'crowd',
            'message': f'Crowd Detected: {count} people'
        })
    return detected_events