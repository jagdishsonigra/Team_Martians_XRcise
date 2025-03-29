import cv2
import mediapipe as mp
from PoseModule import poseDetector
import time

class PhysioExerciseTracker:
    def __init__(self):
        self.detector = poseDetector()
        self.exercise_count = 0
        self.stage = None  
        self.accuracy = 100
        self.current_exercise = "squat" 
        
    def track_jumping_jacks(self, img):
        """
        Track jumping jacks exercise
        Measures angles of both arms and legs
        """
        img = self.detector.findPose(img, False)
        lmList = self.detector.findPosition(img, False)
        
        if len(lmList) != 0:
            # Get landmarks for both arms and legs
            # Left arm: shoulder (11), elbow (13), wrist (15)
            # Right arm: shoulder (12), elbow (14), wrist (16)
            # Left leg: hip (23), knee (25), ankle (27)
            # Right leg: hip (24), knee (26), ankle (28)
            
            # Calculate angles for both arms and legs
            left_arm_angle = self.detector.findAngle(img, 11, 13, 15, True)
            right_arm_angle = self.detector.findAngle(img, 12, 14, 16, True)
            left_leg_angle = self.detector.findAngle(img, 23, 25, 27, True)
            right_leg_angle = self.detector.findAngle(img, 24, 26, 28, True)
            
            # Determine exercise stage based on both arms and legs
            arms_up = left_arm_angle < 90 and right_arm_angle < 90
            legs_spread = left_leg_angle < 90 and right_leg_angle < 90
            
            if arms_up and legs_spread:  # Jumping jack position
                if self.stage == 'down':
                    self.exercise_count += 1
                self.stage = 'up'
                # Calculate accuracy based on how close to 90 degrees
                arm_accuracy = min(100 - abs(left_arm_angle - 90), 100 - abs(right_arm_angle - 90))
                leg_accuracy = min(100 - abs(left_leg_angle - 90), 100 - abs(right_leg_angle - 90))
                self.accuracy = (arm_accuracy + leg_accuracy) / 2
            else:  # Standing position
                self.stage = 'down'
            
            # Display information
            cv2.putText(img, f'Count: {self.exercise_count}', (50, 50), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.putText(img, f'Accuracy: {self.accuracy:.1f}%', (50, 90), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.putText(img, f'Stage: {self.stage}', (50, 130), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            
        return img

    def track_squat(self, img):
        """
        Track squat exercise
        Measures angle between hip, knee, and ankle
        """
        img = self.detector.findPose(img, False)
        lmList = self.detector.findPosition(img, False)
        
        if len(lmList) != 0:
            # Get hip, knee, and ankle landmarks
            # MediaPipe indices: 23 (left hip), 25 (left knee), 27 (left ankle)
            angle = self.detector.findAngle(img, 23, 25, 27, True)
            
            # Determine exercise stage
            if angle > 160:  # Standing up
                if self.stage == 'down':
                    self.exercise_count += 1
                self.stage = 'up'
            elif angle < 70:  # Squatting down
                self.stage = 'down'
                # Calculate accuracy based on how close to 90 degrees
                self.accuracy = max(100 - abs(angle - 90), 0)
            
            # Display information
            cv2.putText(img, f'Count: {self.exercise_count}', (50, 50), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.putText(img, f'Accuracy: {self.accuracy:.1f}%', (50, 90), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.putText(img, f'Stage: {self.stage}', (50, 130), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            
        return img

    def track_shoulder_abduction(self, img):
        """
        Track shoulder abduction exercise
        Measures angle between shoulder, elbow, and wrist
        """
        img = self.detector.findPose(img, False)
        lmList = self.detector.findPosition(img, False)
        
        if len(lmList) != 0:
            # Get shoulder, elbow, and wrist landmarks
            # MediaPipe indices: 11 (left shoulder), 13 (left elbow), 15 (left wrist)
            angle = self.detector.findAngle(img, 11, 13, 15, True)
            
            # Determine exercise stage
            if angle > 160:  # Arm down
                if self.stage == 'up':
                    self.exercise_count += 1
                self.stage = 'down'
            elif angle < 90:  # Arm raised
                self.stage = 'up'
                # Calculate accuracy based on how close to 90 degrees
                self.accuracy = max(100 - abs(angle - 90), 0)
            
            # Display information
            cv2.putText(img, f'Count: {self.exercise_count}', (50, 50), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.putText(img, f'Accuracy: {self.accuracy:.1f}%', (50, 90), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.putText(img, f'Stage: {self.stage}', (50, 130), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            
        return img

    def track_knee_flexion(self, img):
        """
        Track knee flexion/extension exercise
        Measures angle between hip, knee, and ankle
        """
        img = self.detector.findPose(img, False)
        lmList = self.detector.findPosition(img, False)
        
        if len(lmList) != 0:
            # Get hip, knee, and ankle landmarks
            # MediaPipe indices: 23 (left hip), 25 (left knee), 27 (left ankle)
            angle = self.detector.findAngle(img, 23, 25, 27, True)
            
            # Determine exercise stage
            if angle > 160:  # Leg straight
                if self.stage == 'flexed':
                    self.exercise_count += 1
                self.stage = 'extended'
            elif angle < 90:  # Leg bent
                self.stage = 'flexed'
                # Calculate accuracy based on how close to 90 degrees
                self.accuracy = max(100 - abs(angle - 90), 0)
            
            # Display information
            cv2.putText(img, f'Count: {self.exercise_count}', (50, 50), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.putText(img, f'Accuracy: {self.accuracy:.1f}%', (50, 90), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.putText(img, f'Stage: {self.stage}', (50, 130), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            
        return img

    def track_hip_flexion(self, img):
        """
        Track hip flexion/extension exercise
        Measures angle between shoulder, hip, and knee
        """
        img = self.detector.findPose(img, False)
        lmList = self.detector.findPosition(img, False)
        
        if len(lmList) != 0:
            # Get shoulder, hip, and knee landmarks
            # MediaPipe indices: 11 (left shoulder), 23 (left hip), 25 (left knee)
            angle = self.detector.findAngle(img, 11, 23, 25, True)
            
            # Determine exercise stage
            if angle > 160:  # Leg down
                if self.stage == 'flexed':
                    self.exercise_count += 1
                self.stage = 'extended'
            elif angle < 90:  # Leg raised
                self.stage = 'flexed'
                # Calculate accuracy based on how close to 90 degrees
                self.accuracy = max(100 - abs(angle - 90), 0)
            
            # Display information
            cv2.putText(img, f'Count: {self.exercise_count}', (50, 50), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.putText(img, f'Accuracy: {self.accuracy:.1f}%', (50, 90), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.putText(img, f'Stage: {self.stage}', (50, 130), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            
        return img

    def reset_tracking(self):
        """Reset tracking variables for a new exercise"""
        self.exercise_count = 0
        self.stage = None
        self.accuracy = 100

def main():
    cap = cv2.VideoCapture(0)
    tracker = PhysioExerciseTracker()
    
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to grab frame")
            break
            
        # Track current exercise
        if tracker.current_exercise == "squat":
            img = tracker.track_squat(img)
        elif tracker.current_exercise == "shoulder_abduction":
            img = tracker.track_shoulder_abduction(img)
        elif tracker.current_exercise == "knee_flexion":
            img = tracker.track_knee_flexion(img)
        elif tracker.current_exercise == "hip_flexion":
            img = tracker.track_hip_flexion(img)
        elif tracker.current_exercise == "jumping_jacks":
            img = tracker.track_jumping_jacks(img)
        
        # Display current exercise
        cv2.putText(img, f'Exercise: {tracker.current_exercise}', (50, 170), 
                   cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        
        # Display instructions
        cv2.putText(img, '0: Squat', (50, 210), 
                   cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        cv2.putText(img, '1: Shoulder Abduction', (50, 230), 
                   cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        cv2.putText(img, '2: Knee Flexion', (50, 250), 
                   cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        cv2.putText(img, '3: Hip Flexion', (50, 270), 
                   cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        cv2.putText(img, '4: Jumping Jacks', (50, 290), 
                   cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        cv2.putText(img, 'q: Quit', (50, 310), 
                   cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        
        # Display the frame
        cv2.imshow("Physiotherapy Exercise Tracker", img)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('0'):
            tracker.current_exercise = "squat"
            tracker.reset_tracking()
        elif key == ord('1'):
            tracker.current_exercise = "shoulder_abduction"
            tracker.reset_tracking()
        elif key == ord('2'):
            tracker.current_exercise = "knee_flexion"
            tracker.reset_tracking()
        elif key == ord('3'):
            tracker.current_exercise = "hip_flexion"
            tracker.reset_tracking()
        elif key == ord('4'):
            tracker.current_exercise = "jumping_jacks"
            tracker.reset_tracking()
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 