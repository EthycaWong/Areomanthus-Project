import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode
import time
import serial

ser = serial.Serial('/dev/tty.usbserial-0001', 9600, timeout=1)
last_pinch_time = 0
cooldown = 1.0 
is_pinching = False
current_time = time.time()
if current_time - last_pinch_time > cooldown:
     last_pinch_time = current_time


model_path = "hand_landmarker.task"
latest_result = None


def on_result(result, output_image, timestamp_ms):
    global latest_result
    latest_result = result

def detect_pinch(hand_landmarks, w, h):
     global last_pinch_time, is_pinching
     thumb_tip = hand_landmarks[4]
     index_tip = hand_landmarks[8]
     middle_tip = hand_landmarks[12]
     thumb_x = int(thumb_tip.x * w)
     thumb_y = int(thumb_tip.y * h)
     index_x = int(index_tip.x * w)
     index_y = int(index_tip.y * h)
     middle_x = int(middle_tip.x * w)
     middle_y = int(middle_tip.y * h)


     distance = ((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2) ** 0.5
     distance2 = ((thumb_x - middle_x) ** 2 + (thumb_y - middle_y) ** 2) ** 0.5

     current_time = time.time()

     print(f'Balls Distance: {distance:.1f}')


     if distance < 40:
          if not is_pinching and current_time - last_pinch_time > cooldown:
               is_pinching = True
               last_pinch_time = current_time
               ser.write(b'T')
               print(f"Pinch detected! Distance: {distance:.1f}")

     else:
          is_pinching = False
          print(f'Distance: {distance:.1f}')

     if distance2 < 90:
          if not is_pinching and current_time - last_pinch_time > cooldown:
               is_pinching = True
               last_pinch_time = current_time
               ser.write(b'1')
               print(f"Pinch detected! Distance: {distance2:.1f}")

     else:
          is_pinching = False


options = HandLandmarkerOptions(
    base_options = python.BaseOptions(model_asset_path = model_path),
    running_mode = RunningMode.LIVE_STREAM,
    num_hands = 1,
    min_hand_detection_confidence = 0.7,
    min_tracking_confidence = 0.87,
    result_callback = on_result,
)

detector = HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

timestamp = 0


while True:
   ret, frame = cap.read()
   if not ret:
        break
   rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
   detector.detect_async(mp_image, timestamp)
   timestamp += 1
   if latest_result and latest_result.hand_landmarks:
       for hand_landmarks in latest_result.hand_landmarks:
           h, w, c = frame.shape
           detect_pinch(hand_landmarks, w, h)
           x_coords = []
           y_coords = []
           for lm in hand_landmarks:
               x_coords.append(int(lm.x * w))
               y_coords.append(int(lm.y * h))
               x_min, x_max = min(x_coords), max(x_coords)
               y_min, y_max = min(y_coords), max(y_coords)
               
               for id, lm in enumerate(hand_landmarks):
                       x = int(lm.x * w)
                       y = int(lm.y * h)
                       cv2.circle(frame, (x,y), 5, (255, 0, 0), -1)
                       connections = [
                (0,1),(1,2),(2,3),(3,4),
                (0,5),(5,6),(6,7),(7,8),
                (0,9),(9,10),(10,11),(11,12),
                (0,13),(13,14),(14,15),(15,16),
                (0,17),(17,18),(18,19),(19,20),
                (5,9),(9,13),(13,17)
            ]
                       for start, end in connections:
                            x1 = int(hand_landmarks[start].x * w)
                            y1 = int(hand_landmarks[start].y * h)
                            x2 = int(hand_landmarks[end].x * w)
                            y2 = int(hand_landmarks[end].y * h)
                            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
   cv2.imshow('Vision', frame)
   if cv2.waitKey(1) & 0xFF == ord('q'):
       break
detector.close()
cap.release()
cv2.destroyAllWindows()
ser.close()