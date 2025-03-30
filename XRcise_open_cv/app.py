import asyncio
import websockets  # type: ignore
import cv2
import json
import logging
from PhysioExerciseTracker import PhysioExerciseTracker
import time
import base64

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebSocketServer:
    def __init__(self):
        self.tracker = PhysioExerciseTracker()
        self.is_tracking = False
        self.cap = None
        self.frame_interval = 1 / 60  # Increased to 60 FPS
        self.last_frame_time = 0
        self.current_exercise = 'squat'
        self.tracking_task = None

    async def handle_websocket(self, websocket, path=None):
        try:
            logger.info("New client connected")

            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)

                    if data['action'] == 'start':
                        if not self.is_tracking:
                            self.is_tracking = True
                            self.current_exercise = data.get('exercise', 'squat')
                            self.tracker.current_exercise = self.current_exercise
                            self.cap = cv2.VideoCapture(0)

                            # Set camera properties for higher quality and FPS
                            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                            self.cap.set(cv2.CAP_PROP_FPS, 60)
                            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
                            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
                            self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 128)
                            self.cap.set(cv2.CAP_PROP_CONTRAST, 128)
                            self.cap.set(cv2.CAP_PROP_SATURATION, 128)

                            if not self.cap.isOpened():
                                await websocket.send(json.dumps({'error': 'Failed to open camera'}))
                                continue

                            logger.info(f"Camera started successfully for {self.current_exercise}")
                            # Start tracking in a separate task
                            self.tracking_task = asyncio.create_task(self.start_tracking(websocket))
                        else:
                            await websocket.send(json.dumps({'error': 'Tracking is already active'}))

                    elif data['action'] == 'stop':
                        self.is_tracking = False
                        if self.tracking_task:
                            self.tracking_task.cancel()
                            self.tracking_task = None
                        if self.cap:
                            self.cap.release()
                            self.cap = None
                        await websocket.send(json.dumps({
                            'status': 'Tracking stopped',
                            'exercise': self.current_exercise
                        }))

                    elif data['action'] == 'change_exercise':
                        if not self.is_tracking:
                            self.current_exercise = data.get('exercise', 'squat')
                            self.tracker.current_exercise = self.current_exercise
                            self.tracker.reset_tracking()
                            await websocket.send(json.dumps({'status': f'Exercise changed to {self.current_exercise}'}))
                        else:
                            await websocket.send(json.dumps({'error': 'Cannot change exercise while tracking is active'}))

                    elif data['action'] == 'get_status':
                        await websocket.send(json.dumps({
                            'count': self.tracker.exercise_count,
                            'accuracy': self.tracker.accuracy,
                            'stage': self.tracker.stage,
                            'current_exercise': self.current_exercise,
                            'is_tracking': self.is_tracking
                        }))

                except websockets.exceptions.ConnectionClosed:
                    logger.info("Client connection closed")
                    break
                except Exception as e:
                    logger.error(f"Error: {str(e)}")
                    try:
                        await websocket.send(json.dumps({'error': str(e)}))
                    except:
                        pass

        except Exception as e:
            logger.error(f"Error in WebSocket handler: {str(e)}")
        finally:
            if self.tracking_task:
                self.tracking_task.cancel()
            if self.cap:
                self.cap.release()
            logger.info("Client disconnected")

    async def start_tracking(self, websocket):
        while self.is_tracking:
            try:
                current_time = time.time()
                if current_time - self.last_frame_time < self.frame_interval:
                    await asyncio.sleep(0.001)
                    continue

                success, img = self.cap.read()
                if not success:
                    logger.error("Failed to grab frame")
                    continue

                # Resize image for consistent processing while maintaining aspect ratio
                img = cv2.resize(img, (1280, 720))

                # Process the frame based on current exercise
                if self.current_exercise == "squat":
                    img = self.tracker.track_squat(img)
                elif self.current_exercise == "shoulder_abduction":
                    img = self.tracker.track_shoulder_abduction(img)
                elif self.current_exercise == "knee_flexion":
                    img = self.tracker.track_knee_flexion(img)
                elif self.current_exercise == "hip_flexion":
                    img = self.tracker.track_hip_flexion(img)
                elif self.current_exercise == "jumping_jacks":
                    img = self.tracker.track_jumping_jacks(img)

                # Convert frame to base64 with higher quality JPEG encoding
                _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 95])
                frame_base64 = base64.b64encode(buffer).decode('utf-8')

                # Send frame and tracking data together
                await websocket.send(json.dumps({
                    'frame': frame_base64,
                    'count': self.tracker.exercise_count,
                    'accuracy': self.tracker.accuracy,
                    'stage': self.tracker.stage,
                    'current_exercise': self.current_exercise
                }))

                self.last_frame_time = current_time

            except asyncio.CancelledError:
                logger.info("Tracking task cancelled")
                break
            except websockets.exceptions.ConnectionClosed:
                logger.info("Client connection closed during tracking")
                break
            except Exception as e:
                logger.error(f"Error in tracking loop: {str(e)}")
                continue

async def main():
    server = WebSocketServer()
    async with websockets.serve(server.handle_websocket, "192.168.137.227", 9000):
        logger.info("WebSocket server started on ws://192.168.137.227:9000")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
