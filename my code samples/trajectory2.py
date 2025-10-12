"""
Mini Event-based Visual-Inertial Odometry Prototype
Dependencies: opencv-python, numpy
Run: python mini_vio.py
Controls:
  q - quit
  s - toggle saving
  p - pause
"""
import cv2
import numpy as np
import time
from collections import deque

# ---------------- CONFIG ----------------
VIDEO_SOURCE = 0
THRESH_EVENT = 30
EVENT_ACCUM_T = 0.1
MAX_TRAJ = 500
PAUSE = False
SAVE_LOG = False
DT = 0.01  # IMU timestep (s)
# ----------------------------------------

cap = cv2.VideoCapture(VIDEO_SOURCE)
ret, prev = cap.read()
if not ret:
    raise SystemExit("Cannot open video source")

h, w = prev.shape[:2]
prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

# Camera intrinsics
fx = fy = 0.9 * max(h,w)
cx, cy = w/2, h/2
K = np.array([[fx,0,cx],[0,fy,cy],[0,0,1]],dtype=np.float64)

# Optical flow params
feature_params = dict(maxCorners=500, qualityLevel=0.01, minDistance=7, blockSize=7)
lk_params = dict(winSize=(21,21), maxLevel=3,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,30,0.01))

# Buffers
event_buffer = deque()
accum_events = np.zeros((h,w),dtype=np.uint8)
traj = []
p0 = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)

# VIO state
R_cum = np.eye(3)
t_cum = np.zeros((3,1))
# simplified Kalman filter for translation only
P = np.eye(3)*1.0  # covariance
Q = np.eye(3)*0.01 # process noise
R_imu = np.eye(3)*0.1 # IMU noise

last_time = time.time()

# Simulate IMU: rotation rates (rad/s) and acceleration (m/s^2)
imu_rot_rate = np.array([0.0,0.0,0.0])  # roll, pitch, yaw
imu_acc = np.array([0.0,0.0,0.0])       # x, y, z

while True:
    if not PAUSE:
        ret, frame = cap.read()
        if not ret:
            break
        t_now = time.time()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # --- event-like detection ---
        diff = (gray.astype(np.int16) - prev_gray.astype(np.int16))
        pos = diff > THRESH_EVENT
        neg = diff < -THRESH_EVENT
        ys_pos, xs_pos = np.where(pos)
        ys_neg, xs_neg = np.where(neg)
        for (x,y) in zip(xs_pos, ys_pos):
            event_buffer.append((t_now,x,y,1))
            accum_events[y,x] = min(255,accum_events[y,x]+25)
        for (x,y) in zip(xs_neg, ys_neg):
            event_buffer.append((t_now,x,y,-1))
            accum_events[y,x] = min(255,accum_events[y,x]+25)
        # decay
        while event_buffer and (t_now - event_buffer[0][0]) > EVENT_ACCUM_T:
            _,x0,y0,_ = event_buffer.popleft()
            accum_events[y0,x0] = max(0,accum_events[y0,x0]-10)

        # --- sparse tracking ---
        if p0 is None or len(p0)<6:
            p0 = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)

        if p0 is not None:
            p1, st, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, p0, None, **lk_params)
            good0 = p0[st.flatten()==1]
            good1 = p1[st.flatten()==1]
            if len(good0)>=6:
                E, maskE = cv2.findEssentialMat(good1, good0, K, method=cv2.RANSAC, prob=0.999, threshold=1.0)
                if E is not None:
                    _, R, t, _ = cv2.recoverPose(E, good1, good0, K, mask=maskE)
                    # --- SIMULATE IMU ---
                    imu_rot_rate = np.random.randn(3)*0.01  # small rotation noise
                    imu_acc = t.flatten() + np.random.randn(3)*0.01  # noisy translation

                    # --- SIMPLE KALMAN UPDATE ---
                    # predict
                    t_cum = t_cum + imu_acc.reshape(3,1)*DT
                    P = P + Q
                    # update (measurement from visual pose)
                    z = t.flatten().reshape(3,1)
                    K_gain = P @ np.linalg.inv(P+R_imu)
                    t_cum = t_cum + K_gain@(z - t_cum)
                    P = (np.eye(3)-K_gain)@P

                    R_cum = R @ R_cum
                    traj.append((float(t_cum[0]),float(t_cum[2])))

                p0 = good1.reshape(-1,1,2)
        
        prev_gray = gray.copy()
        last_time = t_now

        # --- visualization ---
        heat = cv2.applyColorMap(accum_events, cv2.COLORMAP_JET)
        traj_canvas = np.zeros((h,w,3),dtype=np.uint8)
        center = (w//2, h//2)
        for i in range(1,len(traj)):
            x0 = int(center[0]+traj[i-1][0]*50)
            y0 = int(center[1]-traj[i-1][1]*50)
            x1 = int(center[0]+traj[i][0]*50)
            y1 = int(center[1]-traj[i][1]*50)
            cv2.line(traj_canvas,(x0,y0),(x1,y1),(0,255,255),2)

        cv2.imshow("Event Heat", heat)
        cv2.imshow("Trajectory (x vs z)", traj_canvas)

    key = cv2.waitKey(1)&0xFF
    if key==ord('q'):
        break
    if key==ord('p'):
        PAUSE = not PAUSE

cap.release()
cv2.destroyAllWindows()
