import cv2
import mediapipe as mp
import numpy as np
from config import *

class BlinkDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
            
        # Eye landmarks (left and right eye)
        self.left_eye_indices = [33, 160, 158, 133, 153, 144]
        self.right_eye_indices = [362, 385, 387, 263, 373, 380]
        
        self.ear_history = []
        self.blink_detected = False
        
    def calculate_ear(self, eye_landmarks):
        # Eye Aspect Ratio calculation
        # horizontal eye landmarks
        p1 = np.array([eye_landmarks[0].x, eye_landmarks[0].y])
        p4 = np.array([eye_landmarks[3].x, eye_landmarks[3].y])
        
        # vertical eye landmarks
        p2 = np.array([eye_landmarks[1].x, eye_landmarks[1].y])
        p6 = np.array([eye_landmarks[5].x, eye_landmarks[5].y])
        p3 = np.array([eye_landmarks[2].x, eye_landmarks[2].y])
        p5 = np.array([eye_landmarks[4].x, eye_landmarks[4].y])
        
        # calculate distances
        A = np.linalg.norm(p2 - p6)
        B = np.linalg.norm(p3 - p5)
        C = np.linalg.norm(p1 - p4)
        
        # calculate EAR
        ear = (A + B) / (2.0 * C)
        return ear
        
    def process_frame(self, frame):
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            return {'blink_detected': False}
            
        face_landmarks = results.multi_face_landmarks[0]
        
        # Get left and right eye landmarks
        left_eye = [face_landmarks.landmark[i] for i in self.left_eye_indices]
        right_eye = [face_landmarks.landmark[i] for i in self.right_eye_indices]
        
        # Calculate EAR for both eyes
        left_ear = self.calculate_ear(left_eye)
        right_ear = self.calculate_ear(right_eye)
        avg_ear = (left_ear + right_ear) / 2.0
        
        # Detect blink
        self.ear_history.append(avg_ear)
        if len(self.ear_history) > EAR_CONSECUTIVE_FRAMES:
            self.ear_history.pop(0)
            
        # Check if EAR is below threshold for consecutive frames
        blink_detected = all(ear < EAR_THRESHOLD for ear in self.ear_history)
        
        # Only trigger once per blink
        result = False
        if blink_detected and not self.blink_detected:
            result = True
            
        self.blink_detected = blink_detected
        
        return {
            'blink_detected': result,
            'ear': avg_ear
        }
        
    def __del__(self):
        self.face_mesh.close()