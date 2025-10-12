"""
Mini continuous-time reprojection-error VIO prototype
Dependencies: opencv-python, numpy
Run: python event_vio_proto.py
Controls:
  q - quit
  p - pause
"""

import cv2
import numpy as np
import time
from collections import deque

# ---------- CONFIG ----------
VIDEO_SOURCE = 0
THRESH_EVENT = 30
EVENT_ACCUM_T = 0.1
MAX_TRAJ = 500
PAUSE = False
# pseudo-IMU gains (just for demo)
ACC_GAIN = 0.01
GYRO_GAIN = 0.005
# ----------------------------

cap = cv2.VideoCapture(VIDEO_SOURCE)
ret, prev = cap.read()
if not ret:
    raise SystemExit("Cannot open video source")

h, w = prev.shape[:2]
prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

# event buffer
event_buffer = deque()
accum_events = np.zeros((h, w), dtype=np.uint8)
traj = []
# 6-DOF cumulative pose
R_cum = np.eye(3)
t_cum = np.zeros((3,1))
last_time = time.time()

# pseudo-IMU state
imu_gyro = np.zeros(3)   # rotational velocity
imu_acc = np.zeros(3)    # linear acceleration

# features for sparse optical flow
feature_params = dict(maxCorners=1000, qualityLevel=0.01, minDistance=7, blockSize=7)
lk_params = dict(winSize=(21,21), maxLevel=3,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))
p0 = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)

while True:
    if not PAUSE:
        ret, frame = cap.read()
        if not ret:
            break
        t_now = time.time()
        dt = t_now - last_time
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # --- event-like generation ---
        diff = gray.astype(np.int16) - prev_gray.astype(np.int16)
        pos = diff > THRESH_EVENT
        neg = diff < -THRESH_EVENT

        ys_pos, xs_pos = np.where(pos)
        ys_neg, xs_neg = np.where(neg)

        for (x,y) in zip(xs_pos, ys_pos):
            event_buffer.append((t_now, x, y, 1))
            accum_events[y,x] = min(255, accum_events[y,x]+25)
        for (x,y) in zip(xs_neg, ys_neg):
            event_buffer.append((t_now, x, y, -1))
            accum_events[y,x] = min(255, accum_events[y,x]+25)

        # prune old events
        while event_buffer and (t_now - event_buffer[0][0]) > EVENT_ACCUM_T:
            _, x0, y0, _ = event_buffer.popleft()
            accum_events[y0,x0] = max(0, accum_events[y0,x0]-10)

        # --- sparse tracking ---
        if p0 is None or len(p0)<6:
            p0 = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)
        if p0 is not None and len(p0)>=6:
            p1, st, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, p0, None, **lk_params)
            good0 = p0[st.flatten()==1]
            good1 = p1[st.flatten()==1]

            # --- pseudo 6-DOF pose update ---
            # rotation from optical flow (simplified)
            if len(good0)>=6:
                flow = good1 - good0
                avg_flow = np.mean(flow, axis=0)
                # gyro-like rotation update
                dR = np.eye(3)
                dR[:2,2] = avg_flow * GYRO_GAIN
                R_cum = dR @ R_cum

                # translation from pseudo-IMU (integrate accelerometer)
                imu_acc += np.random.randn(3)*0.5   # simulate some accelerometer noise
                dt_vec = imu_acc * dt * ACC_GAIN
                t_cum += R_cum @ dt_vec.reshape(3,1)

                # store x,z for 2D trajectory
                traj.append((float(t_cum[0]), float(t_cum[2])))

            p0 = good1.reshape(-1,1,2)
        
        prev_gray = gray.copy()
        last_time = t_now

        # --- visualization ---
        heat = cv2.applyColorMap(accum_events, cv2.COLORMAP_JET)
        traj_canvas = np.zeros((h,w,3),dtype=np.uint8)
        center = (w//2,h//2)
        pts = traj[-MAX_TRAJ:]
        for i in range(1,len(pts)):
            x0 = int(center[0]+pts[i-1][0]*50)
            y0 = int(center[1]-pts[i-1][1]*50)
            x1 = int(center[0]+pts[i][0]*50)
            y1 = int(center[1]-pts[i][1]*50)
            cv2.line(traj_canvas,(x0,y0),(x1,y1),(0,255,255),2)

        overlay = frame.copy()
        cv2.putText(overlay,f'Events:{len(xs_pos)+len(xs_neg)}', (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0,0,255),2)
        combined = np.hstack((overlay,heat))
        cv2.imshow('Overlay | Event Heat', combined)
        cv2.imshow('Trajectory (x vs z)', traj_canvas)

    key = cv2.waitKey(1)&0xFF
    if key==ord('q'):
        break
    if key==ord('p'):
        PAUSE = not PAUSE

cap.release()
cv2.destroyAllWindows()
