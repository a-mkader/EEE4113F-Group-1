import cv2
import time
import threading
from adafruit_servokit import ServoKit
from sshkeyboard import listen_keyboard, stop_listening
from pid import PID

# Enable OpenCV optimizations
cv2.setUseOptimized(True)

# Initialize the ServoKit
kit = ServoKit(channels=16)

# Set default angles for pan and tilt
pan_angle = 90
tilt_angle = 90

kit.servo[0].angle = pan_angle
kit.servo[1].angle = tilt_angle

# Initialize PID controllers for pan and tilt
pan_pid = PID(Kp=1.1, Ki=0.001, Kd=0.003, output_limits=(-3, 3))
tilt_pid = PID(Kp=1.1, Ki=0.001, Kd=0.003, output_limits=(-3, 3))

# Keyboard control flags
release_a = False
release_d = False
release_w = False
release_s = False
loop = True

def press(key):
    global loop, pan_angle, tilt_angle, release_a, release_d, release_w, release_s

    if key == 'q':
        loop = False

    if key == "w":
        release_w = False
        while tilt_angle > 15 and not release_w:
            tilt_angle -= 1
            kit.servo[1].angle = tilt_angle
            time.sleep(0.01)

    elif key == "s":
        release_s = False
        while tilt_angle < 180 and not release_s:
            tilt_angle += 1
            kit.servo[1].angle = tilt_angle
            time.sleep(0.01)

    elif key == "a":
        release_a = False
        while pan_angle < 180 and not release_a:
            pan_angle += 1
            kit.servo[0].angle = pan_angle
            time.sleep(0.01)

    elif key == "d":
        release_d = False
        while pan_angle > 0 and not release_d:
            pan_angle -= 1
            kit.servo[0].angle = pan_angle
            time.sleep(0.01)

def release(key):
    global release_a, release_d, release_w, release_s

    if key == "w":
        release_w = True

    elif key == "s":
        release_s = True

    elif key == "a":
        release_a = True

    elif key == "d":
        release_d = True

def input_keyboard():
    listen_keyboard(
        on_press=press,
        on_release=release,
        delay_second_char=0.001
    )

keyboard_thread = threading.Thread(target=input_keyboard)
keyboard_thread.daemon = True
keyboard_thread.start()

# Connect to RTSP stream (consider lowering RTSP resolution via camera if possible)
cap = cv2.VideoCapture("rtsp://192.168.0.70:8554/cam")

ret, img = cap.read()
if not ret:
    print("Failed to grab first frame from RTSP stream.")
    exit(1)

# Determine the target resolution based on aspect ratio
if img.shape[1]/img.shape[0] > 1.55:
    res = (256, 144)
else:
    res = (216, 162)

# Precompute tracking center positions
XC = res[0] / 2
YC = res[1] * 7 / 16

# Load Haar cascade classifier
cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")

# Frame processing control
frame_interval = 0.1  # seconds for ~10 FPS
last_time = time.time()
frame_count = 0
detect_interval = 3  # run face detection every 3 frames

# Control display window (set False to disable if using VNC for less lag)
show_window = True

while loop:
    ret, img = cap.read()
    if not ret:
        print("Failed to grab frame.")
        time.sleep(0.1)
        continue

    now = time.time()
    if now - last_time < frame_interval:
        # Skip frames to maintain target FPS
        continue
    last_time = now
    frame_count += 1

    # Resize early for efficiency
    resized = cv2.resize(img, res, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # Run detection only every detect_interval frames
    if frame_count % detect_interval == 0:
        faces = cascade.detectMultiScale(gray)
    else:
        faces = []

    if len(faces) > 0:
        x, y, w, h = faces[0]  # Use first detected face
        center = (x + w / 2, y + h / 2)

        # PID control based on error between face center and desired center
        pan_error = XC - center[0]
        tilt_error = YC - center[1]

        pan_adjust = pan_pid.compute(pan_error, now)
        tilt_adjust = tilt_pid.compute(tilt_error, now)

        # Update angles with clamp
        pan_angle = max(0, min(180, pan_angle + pan_adjust))
        tilt_angle = max(0, min(180, tilt_angle + tilt_adjust))

        kit.servo[0].angle = pan_angle
        kit.servo[1].angle = tilt_angle

        if show_window:
            # Draw rectangle and center point
            cv2.rectangle(resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(resized, (int(center[0]), int(center[1])), 3, (0, 0, 255), -1)

        print(f"pan_error: {pan_error:.2f}, pan_adjust: {pan_adjust:.2f}, pan_angle: {pan_angle:.2f}")
        print(f"tilt_error: {tilt_error:.2f}, tilt_adjust: {tilt_adjust:.2f}, tilt_angle: {tilt_angle:.2f}")

    else:
        if show_window:
            cv2.putText(resized, "No face detected", (10, res[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

   # if show_window:
        #cv2.imshow("Face Tracker", resized)
        # Use waitKey(1) for responsive GUI and key event polling
        #if cv2.waitKey(1) & 0xFF == ord('q'):
         #   loop = False

# Clean up
cap.release()
#cv2.destroyAllWindows()
stop_listening()
keyboard_thread.join()
print("Exiting")
