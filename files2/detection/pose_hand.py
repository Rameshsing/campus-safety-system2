import mediapipe as mp
import cv2
import time

mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def detect_pose_hand(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pose_results = pose.process(rgb)
    hand_results = hands.process(rgb)
    events = []
    if hand_results.multi_hand_landmarks:
        events.append({
            'timestamp': time.time(),
            'type': 'hand',
            'message': 'Hand(s) Detected'
        })
    # Simple hands raised detection
    if pose_results.pose_landmarks:
        lmk = pose_results.pose_landmarks.landmark
        left_wrist = lmk[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = lmk[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        left_shoulder = lmk[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = lmk[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        if (left_wrist.y < left_shoulder.y) and (right_wrist.y < right_shoulder.y):
            events.append({
                'timestamp': time.time(),
                'type': 'pose',
                'message': 'Both Hands Raised'
            })
    return events

def detect_fall(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pose_results = pose.process(rgb)
    events = []
    if pose_results.pose_landmarks:
        lmk = pose_results.pose_landmarks.landmark
        left_hip = lmk[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = lmk[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_shoulder = lmk[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = lmk[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        if (left_hip.y > left_shoulder.y) and (right_hip.y > right_shoulder.y):
            events.append({
                'timestamp': time.time(),
                'type': 'fall',
                'message': 'Possible Fall Detected'
            })
    return events