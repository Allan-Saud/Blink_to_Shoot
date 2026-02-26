import cv2
import mediapipe as mp

class FaceTracker:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        
    def process_frame(self, frame):
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            return None
            
        # Get nose tip (landmark 1)
        face_landmarks = results.multi_face_landmarks[0]
        nose = face_landmarks.landmark[1]
        
        return {
            'nose_x': nose.x,
            'nose_y': nose.y
        }
        
    def __del__(self):
        self.face_mesh.close()