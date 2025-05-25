import cv2
import time
import threading
import subprocess
import os
import signal
from adafruit_servokit import ServoKit
from sshkeyboard import listen_keyboard, stop_listening
from pid import PID

def setup_virtual_camera():
    subprocess.run(["sudo", "modprobe", "-r", "v4l2loopback"], stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "modprobe", "v4l2loopback", "video_nr=30", "card_label=VirtualCam", "exclusive_caps=1"])
    
    # Start GStreamer pipeline
    gst_cmd = (
    "gst-launch-1.0 libcamerasrc ! "
    "video/x-raw,width=640,height=480,framerate=30/1 ! "
    "videoconvert ! video/x-raw,format=YUY2 ! "
    "v4l2sink device=/dev/video30"
    )

    return subprocess.Popen(gst_cmd, shell=True, preexec_fn=os.setsid)
    
def start_mediamtx():
    return subprocess.Popen(
        ["./mediamtx"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid
    )

# ----------- Setup Stage -------------
gst_proc = setup_virtual_camera()
# Start MediaMTX
mediamtx_proc = subprocess.Popen(["./mediamtx"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(3)  # Allow time for /dev/video30

cv2.setUseOptimized(True)
kit = ServoKit(channels=16)
pan_angle = 90
tilt_angle = 90
kit.servo[0].angle = pan_angle
kit.servo[1].angle = tilt_angle

pan_pid = PID(Kp=10, Ki=0.5, Kd=2.5, output_limits=(-5, 5))
tilt_pid = PID(Kp=10, Ki=0.5, Kd=2.5, output_limits=(-5, 5))

release_a = release_d = release_w = release_s = False
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
    if key == "w": release_w = True
    elif key == "s": release_s = True
    elif key == "a": release_a = True
    elif key == "d": release_d = True

keyboard_thread = threading.Thread(target=lambda: listen_keyboard(on_press=press, on_release=release, delay_second_char=0.001))
keyboard_thread.daemon = True
keyboard_thread.start()

cap = cv2.VideoCapture("/dev/video30")
ret, img = cap.read()
if not ret:
    print("Failed to grab first frame.")
    gst_proc.terminate()
    start_mediamtx()
    exit(1)

res = (256, 144) if img.shape[1]/img.shape[0] > 1.55 else (216, 162)
scale_factor = 3
XC = res[0] / 2
YC = res[1] * 7 / 16

vcam_writer = cv2.VideoWriter('/dev/video30', cv2.VideoWriter_fourcc(*'MJPG'), 30, res)

# Start RTSP streaming using FFmpeg to MediaMTX
stream_proc = subprocess.Popen(
    [
        'ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', f'{res[0]}x{res[1]}',
        '-r', '30',
        '-i', '-',
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-f', 'rtsp',
        'rtsp://192.168.0.71:8554/cam'
    ],
    stdin=subprocess.PIPE
)

cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")

frame_interval = 0.05
last_time = time.time()
frame_count = 0
detect_interval = 1
show_window = True

while loop:
    ret, img = cap.read()
    if not ret:
        print("Failed to grab frame.")
        time.sleep(0.1)
        continue

    now = time.time()
    if now - last_time < frame_interval:
        continue
    last_time = now
    frame_count += 1

    resized = cv2.resize(img, res, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # --- Detect face ---
    if frame_count % detect_interval == 0:
        faces = cascade.detectMultiScale(gray)
    else:
        faces = []

    # --- If face found, track ---
    if len(faces) > 0:
        x, y, w, h = faces[0]
        center = (x + w / 2, y + h / 2)
        pan_error = XC - center[0]
        tilt_error = YC - center[1]

        pan_adjust = pan_pid.compute(pan_error, now) if abs(pan_error) > 10 else 0
        tilt_adjust = tilt_pid.compute(tilt_error, now) if abs(tilt_error) > 10 else 0

        pan_angle = max(0, min(180, pan_angle + pan_adjust))
        tilt_angle = max(0, min(180, tilt_angle + tilt_adjust))
        kit.servo[0].angle = pan_angle
        kit.servo[1].angle = tilt_angle

        if show_window:
            cv2.rectangle(resized, (x, y), (x + w, y + h), (0, 255, 0), 1)

        print(f"pan_error: {pan_error:.2f}, pan_adjust: {pan_adjust or 0:.2f}, pan_angle: {pan_angle:.2f}")
        print(f"tilt_error: {tilt_error:.2f}, tilt_adjust: {tilt_adjust or 0:.2f}, tilt_angle: {tilt_angle:.2f}")


    else:
        if show_window:
            cv2.putText(resized, "No face detected", (10, res[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

    # --- Write to BOTH RTSP and Virtual Cam ---
    stream_proc.stdin.write(resized.tobytes())
    vcam_writer.write(resized)

    # --- Show preview window ---
    if show_window:
        display_img = cv2.resize(resized, (res[0]*scale_factor, res[1]*scale_factor), interpolation=cv2.INTER_NEAREST)
        cv2.imshow("Face Tracker", display_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            loop = False

# ----------- Cleanup -------------
cap.release()
cv2.destroyAllWindows()
stop_listening()
keyboard_thread.join()
vcam_writer.release()
os.killpg(os.getpgid(gst_proc.pid), signal.SIGTERM)
stream_proc.terminate()
mediamtx_proc.terminate()
print("Exiting")
