import cv2
import numpy as np
import time
import socket
import PoseModule as pm

class ExerciseTrainer:
    video_paths = {
        "Squat": "squat.mp4",
        "Shoulder Abduction": "shoulder_abduction.mp4",
        "Knee Flexion": "knee_flexion.mp4",
        "Hip Flexion": "hip_flexion.mp4",
        "Jumping Jack": "jumpingjack.mp4"
    }
    
    exercise_params = {
        "Squat": {
            "landmarks": [23, 25, 27, 24, 26, 28],  # Both legs  
            "angle_points": [24, 26, 28],  # Right leg (hip, knee, ankle)
            "angle_range": (70, 160),  # Adjusted for squat range
            "percent_range": (0, 100),
            "bar_range": (650, 100)
        },
        "Shoulder Abduction": {
            "landmarks": [11, 13, 15, 12, 14, 16],  # Both arms
            "angle_points": [11, 13, 15],  # Left arm (shoulder, elbow, wrist)
            "angle_range": (90, 160),  # Adjusted for shoulder abduction
            "percent_range": (0, 100),
            "bar_range": (650, 100)
        },
        "Knee Flexion": {
            "landmarks": [23, 25, 27, 24, 26, 28],  # Both legs
            "angle_points": [23, 25, 27],  # Left leg (hip, knee, ankle)
            "angle_range": (90, 160),  # Adjusted for knee flexion
            "percent_range": (0, 100),
            "bar_range": (650, 100)
        },
        "Hip Flexion": {
            "landmarks": [11, 23, 25, 12, 24, 26],  # Both sides
            "angle_points": [11, 23, 25],  # Left side (shoulder, hip, knee)
            "angle_range": (90, 160),  # Adjusted for hip flexion
            "percent_range": (0, 100),
            "bar_range": (650, 100)
        },
        "Jumping Jack": {
            "landmarks": [11, 13, 15, 12, 14, 16, 23, 25, 27, 24, 26, 28],
            "angle_points": [11, 13, 15],  # Left arm (shoulder, elbow, wrist)
            "angle_range": (90, 180),  # Adjusted for jumping jack
            "percent_range": (0, 100),
            "bar_range": (650, 100)
        }
    }

    def __init__(self):
        self.cap = cv2.VideoCapture(0)  # Use webcam
        self.detector = pm.poseDetector()
        self.count = 0
        self.dir = 0
        self.pTime = 0
        self.params = None
        self.stage = None
        self.accuracy = 100
        
        # Set up socket connection
        self.HOST = '0.0.0.0'  # Listen on all network interfaces
        self.PORT = 5005        # Choose a free port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen(1)
        print(f"Waiting for Unity to connect on {self.HOST}:{self.PORT}...")

    def receive_exercise_choice(self, conn):
        """Receive the exercise name from Unity."""
        exercise_choice = conn.recv(1024).decode('utf-8').strip()
        return exercise_choice

    def calculate_exercise_metrics(self, img, lmList):
        """Calculate exercise metrics (angle, percentage, bar position)."""
        if not lmList or len(lmList) < 33:
            return None, None, None
            
        # Calculate angle
        points = self.params["angle_points"]
        angle = self.detector.findAngle(img, points[0], points[1], points[2])
        
        # Calculate percentage and bar position
        per = np.interp(angle, self.params["angle_range"], self.params["percent_range"])
        bar = np.interp(angle, self.params["angle_range"], self.params["bar_range"])
                       
        return angle, per, bar

    def determine_exercise_stage(self, angle, exercise):
        """Determine the current stage of the exercise based on angle."""
        if exercise == "Squat":
            if angle > 150:  # Standing up
                if self.stage == 'down':
                    self.count += 1
                self.stage = 'up'
            elif angle < 100:  # Squatting down
                self.stage = 'down'
        elif exercise == "Shoulder Abduction":
            if angle > 160:  # Arm down
                if self.stage == 'up':
                    self.count += 1
                self.stage = 'down'
            elif angle < 90:  # Arm raised
                self.stage = 'up'
        elif exercise == "Knee Flexion":
            if angle > 160:  # Leg straight
                if self.stage == 'flexed':
                    self.count += 1
                self.stage = 'extended'
            elif angle < 90:  # Leg bent
                self.stage = 'flexed'
        elif exercise == "Hip Flexion":
            if angle > 160:  # Leg down
                if self.stage == 'flexed':
                    self.count += 1
                self.stage = 'extended'
            elif angle < 90:  # Leg raised
                self.stage = 'flexed'
        elif exercise == "Jumping Jack":
            if angle > 160:  # Standing position
                if self.stage == 'up':
                    self.count += 1
                self.stage = 'down'
            elif angle < 90:  # Arms up
                self.stage = 'up'

    def display_tracking_info(self, img, per, bar, exercise):
        """Display tracking information on the video feed."""
        # Color based on form
        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
        if per == 0:
            color = (0, 255, 0)
                
        # Draw Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

        # Draw Exercise Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(self.count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)
        
        # Draw Stage
        if self.stage:
            cv2.putText(img, f'Stage: {self.stage}', (50, 130), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        
        # Draw Exercise Name
        cv2.putText(img, f'Exercise: {exercise}', (50, 170), 
                   cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    def track_exercise(self, conn, exercise):
        """Track the specified exercise and send metrics to Unity."""
        self.params = self.exercise_params.get(exercise, None)
        if not self.params:
            print(f"Exercise '{exercise}' not found.")
            return

        while True:
            success, img = self.cap.read()
            if not success:
                break
                
            img = cv2.resize(img, (1280, 720))
            img = self.detector.findPose(img, True)
            lmList = self.detector.findPosition(img, False)
            
            if lmList and self.params:
                # Calculate exercise metrics
                angle, per, bar = self.calculate_exercise_metrics(img, lmList)
                
                if angle is not None:
                    # Determine exercise stage
                    self.determine_exercise_stage(angle, exercise)
                    
                    # Display tracking information
                    self.display_tracking_info(img, per, bar, exercise)
                    
                    # Send metrics to Unity
                    message = f"{angle:.2f},{per:.2f},{bar:.2f},{int(self.count)}\n"
                    try:
                        conn.sendall(message.encode('utf-8'))
                    except (ConnectionResetError, BrokenPipeError):
                        print("Client disconnected.")
                        break
                    
                    # Draw reference points for visualization
                    for landmark_idx in self.params["landmarks"]:
                        if landmark_idx < len(lmList):
                            cv2.circle(img, (lmList[landmark_idx][1], lmList[landmark_idx][2]), 10, (255, 0, 0), cv2.FILLED)
            
            # Display FPS
            cTime = time.time()
            fps = 1 / (cTime - self.pTime)
            self.pTime = cTime
            cv2.putText(img, f'FPS: {int(fps)}', (50, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            
            cv2.imshow("AI Trainer", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        self.cap.release()
        cv2.destroyAllWindows()
        conn.close()

    def start_server(self):
        """Start the server and handle client connections."""
        while True:
            print("Waiting for a new client to connect...")
            conn, addr = self.server_socket.accept()
            print(f"Connected to Unity at {addr}")

            try:
                # Receive exercise choice from Unity
                exercise = self.receive_exercise_choice(conn)
                print(f"Starting exercise: {exercise}")

                # Reset tracking variables
                self.count = 0
                self.dir = 0
                self.stage = None
                self.accuracy = 100

                # Track the exercise
                self.track_exercise(conn, exercise)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                print("Client disconnected. Resetting for new connection...")
                self.count = 0
                self.dir = 0
                self.params = None
                self.stage = None
                self.accuracy = 100

if __name__ == "__main__":
    trainer = ExerciseTrainer()
    trainer.start_server() 