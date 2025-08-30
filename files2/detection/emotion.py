import time
from deepface import DeepFace

DISTRESS_EMOTIONS = ['fear', 'angry', 'sad']

def detect_emotion(frame):
    events = []
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result['dominant_emotion']
        if emotion in DISTRESS_EMOTIONS:
            events.append({
                'timestamp': time.time(),
                'type': 'distress',
                'message': f'Distress Detected: {emotion.capitalize()}'
            })
    except Exception as e:
        pass
    return events