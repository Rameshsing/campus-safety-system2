import time
from deepface import DeepFace

BLACKLIST = ["John Doe", "Jane Blacklist"]  # Replace with actual names/faces

def detect_faces(frame):
    events = []
    try:
        results = DeepFace.find(img_path=frame, db_path="face_db", enforce_detection=False)
        for result in results:
            identity = result['identity']
            if identity in BLACKLIST:
                events.append({
                    'timestamp': time.time(),
                    'type': 'blacklist',
                    'message': f'Blacklisted Person Detected: {identity}'
                })
    except Exception as e:
        pass
    return events