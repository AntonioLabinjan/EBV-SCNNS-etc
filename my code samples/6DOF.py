"""
Event-like 6-DOF prototype
Dependencies: opencv-python, numpy
Run: python event_6dof_sim.py
Controls:
  q - quit
  s - toggle saving events/logging
  p - pause
"""


'''

1. **Ulaz i inicijalizacija**

   * Otvara video iz kamere (ili drona) i čita prvi frame.
   * Postavlja parametre kamere (K-matricu) i priprema tracking featurea (Shi-Tomasi + Lucas-Kanade).

2. **Event-like detekcija**

   * Svaki novi frame uspoređuje s prethodnim pixel-by-pixel.
   * Ako je promjena veća od `THRESH_EVENT`, generira se *event* (pozitivan ili negativan).
   * Time se simulira način rada event kamere (asinkrono, promjena → event).

3. **Akumulacija događaja (event buffer)**

   * Sprema sve evente unutar vremenskog prozora `EVENT_ACCUM_T`.
   * Svaki pixel kojem se promjena često događa "svijetli" jače na heatmapi.
   * Stari eventi se gase s vremenom (decay efekt).

4. **Sparse optical flow tracking**

   * Prati male feature točke između frameova pomoću Lucas-Kanade metode.
   * Ako nema dovoljno točaka, ponovno ih detektira.
   * Održava stabilan set točaka kroz vrijeme.

5. **Estimacija kamere (6-DOF)**

   * Iz para frameova izračuna *Essential matrix* pomoću RANSAC-a.
   * Iz nje rekonstruira **rotaciju (R)** i **translaciju (t)** kamere (pose recovery).
   * Rezultat: kamera se “miče” u 3D prostoru (do skale).

6. **Integracija kretanja**

   * Zbraja svaku novu translaciju i rotaciju s prethodnima (R_cum, t_cum).
   * Tako se gradi “trajektorija” kretanja kamere kroz prostor.

7. **Vizualizacija matchova i eventa**

   * Lijeva strana prozora prikazuje optical flow linije (veze između frameova).
   * Desna strana prikazuje heatmapu eventova u zadnjih par stotinki sekunde.

8. **Trajektorija kretanja**

   * Poseban prozor crta 2D mapu kretanja (x-z ravnina) kamere u prostoru.
   * Pokazuje smjer i duljinu translacije (poput mini-SLAM vizualizacije).

9. **Logiranje i FPS**

   * Sprema sve podatke u CSV: broj eventova, broj matchova, matrice rotacije i translacije, FPS.
   * Korisno za kasniju analizu pokreta ili treniranje modela.

10. **Kontrole i interakcija**

* `q` → quit
* `p` → pauza
* `s` → uključi/isključi logiranje
* `r` → resetiraj trajektoriju i integraciju

---

Ukratko — ovaj kod simulira **event kameru** pomoću obične web kamere i istovremeno izvlači **6-DOF kretanje** pomoću *optical flowa* i *pose estimacije*.
To je kao mali “vizualni inercijalni odometar” koji sve to crta u realnom vremenu. 

'''
import cv2
import numpy as np
import time
import csv
from collections import deque

# -------- CONFIG ----------
VIDEO_SOURCE = 0              # 0 = laptop camera, or "drone_highspeed.mp4"
THRESH_EVENT = 30            # threshold for event-like differencing
EVENT_ACCUM_T = 0.1          # seconds: accumulate events in this time window for visualization
MAX_TRAJ = 500               # max points to draw trajectory
LOG_FILE = "pose_log.csv"
SAVE_LOG = True
# ---------------------------

cap = cv2.VideoCapture(VIDEO_SOURCE)
ret, prev = cap.read()
if not ret:
    raise SystemExit("Cannot open video source")

h, w = prev.shape[:2]
# Simple intrinsics approximation (monocular, should be tuned for real camera)
fx = fy = 0.9 * max(w, h)
cx, cy = w/2, h/2
K = np.array([[fx, 0, cx],
              [0, fy, cy],
              [0,  0,  1]], dtype=np.float64)

prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

# For sparse tracking
feature_params = dict(maxCorners=1000, qualityLevel=0.01, minDistance=7, blockSize=7)
lk_params = dict(winSize=(21,21), maxLevel=3,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))

# buffers
event_buffer = deque()  # (t, x, y, polarity)
accum_events = np.zeros((h, w), dtype=np.uint8)
traj = []               # integrated camera positions (up to scale)
R_cum = np.eye(3)       # cumulative rotation
t_cum = np.zeros((3,1)) # cumulative translation (up to scale)
last_time = time.time()
paused = False
saving = SAVE_LOG

# logging
if SAVE_LOG:
    f_log = open(LOG_FILE, "w", newline="")
    writer = csv.writer(f_log)
    writer.writerow(["timestamp","num_events","num_matches","r11","r12","r13","r21","r22","r23","r31","r32","r33","tx","ty","tz","fps"])

# initial good features
p0 = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)

while True:
    if not paused:
        ret, frame = cap.read()
        if not ret:
            break
        t_now = time.time()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # --- event-like generation (per-pixel diff) ---
        diff = (gray.astype(np.int16) - prev_gray.astype(np.int16))
        pos = (diff > THRESH_EVENT)
        neg = (diff < -THRESH_EVENT)
        polarity = np.zeros_like(diff, dtype=np.int8)
        polarity[pos] = 1
        polarity[neg] = -1

        ys_pos, xs_pos = np.where(pos)
        ys_neg, xs_neg = np.where(neg)

        for (x,y) in zip(xs_pos, ys_pos):
            event_buffer.append((t_now, x, y, 1))
            accum_events[y,x] = min(255, accum_events[y,x] + 25)
        for (x,y) in zip(xs_neg, ys_neg):
            event_buffer.append((t_now, x, y, -1))
            accum_events[y,x] = min(255, accum_events[y,x] + 25)

        # prune event buffer and decay accum_events
        while event_buffer and (t_now - event_buffer[0][0]) > EVENT_ACCUM_T:
            _, x0, y0, _ = event_buffer.popleft()
            accum_events[y0,x0] = max(0, accum_events[y0,x0] - 10)

        # --- sparse tracking (Shi-Tomasi + LK) ---
        if p0 is None or len(p0) < 50:
            p0 = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)

        if p0 is not None and len(p0) >= 6:
            p1, st, err = cv2.calcOpticalFlowPyrLK(prev_gray, gray, p0, None, **lk_params)
            good0 = p0[st.flatten()==1]
            good1 = p1[st.flatten()==1]
            if len(good0) >= 6:
                # Essential matrix + recoverPose
                E, maskE = cv2.findEssentialMat(good1, good0, K, method=cv2.RANSAC, prob=0.999, threshold=1.0)
                if E is not None:
                    inliers, R, t, mask_pose = cv2.recoverPose(E, good1, good0, K, mask=maskE)
                    # Integrate pose (note: t up to scale). We'll scale t by inliers (heuristic) for visualization
                    scale = max(0.001, inliers/50.0)  # heuristic scale factor (purely visual)
                    t_scaled = t * scale

                    # update cumulative
                    t_cum = t_cum + R_cum.dot(t_scaled)
                    R_cum = R.dot(R_cum)

                    # save simple traj point (x,z) for display (use x and z)
                    traj.append((float(t_cum[0]), float(t_cum[2])))

                    num_matches = int(len(good0))
                    # logging
                    fps = 1.0 / max(1e-6, (t_now - last_time))
                    if saving:
                        writer.writerow([t_now, len(xs_pos)+len(xs_neg), num_matches,
                                         R[0,0],R[0,1],R[0,2],R[1,0],R[1,1],R[1,2],R[2,0],R[2,1],R[2,2],
                                         float(t_cum[0]), float(t_cum[1]), float(t_cum[2]), fps])
                else:
                    num_matches = int(len(good0))
                    fps = 1.0 / max(1e-6, (t_now - last_time))
                    if saving:
                        writer.writerow([t_now, len(xs_pos)+len(xs_neg), num_matches] + ["nan"]*12 + [fps])

                # draw matches on overlay
                overlay = frame.copy()
                for (pt0, pt1) in zip(good0, good1):
                    x0,y0 = pt0.ravel().astype(int)
                    x1,y1 = pt1.ravel().astype(int)
                    cv2.line(overlay, (x0,y0), (x1,y1), (0,255,0), 1)
                    cv2.circle(overlay, (x1,y1), 2, (0,255,0), -1)
            else:
                overlay = frame.copy()
                num_matches = 0
                if saving:
                    writer.writerow([t_now, len(xs_pos)+len(xs_neg), num_matches] + ["nan"]*12 + [1.0/(t_now-last_time+1e-6)])
            p0 = good1.reshape(-1,1,2) if (p1 is not None and st is not None) else None
        else:
            overlay = frame.copy()
            num_matches = 0
            if saving:
                writer.writerow([t_now, len(xs_pos)+len(xs_neg), num_matches] + ["nan"]*12 + [1.0/(t_now-last_time+1e-6)])

        # --- visualizations ---
        # events heatmap (accumulated)
        heat = cv2.applyColorMap(accum_events, cv2.COLORMAP_JET)
        # trajectory canvas
        traj_canvas = np.zeros((h, w, 3), dtype=np.uint8)
        # draw trajectory (center at frame)
        center = (w//2, h//2)
        pts = traj[-MAX_TRAJ:]
        for i in range(1, len(pts)):
            x0 = int(center[0] + pts[i-1][0]*50)
            y0 = int(center[1] - pts[i-1][1]*50)
            x1 = int(center[0] + pts[i][0]*50)
            y1 = int(center[1] - pts[i][1]*50)
            cv2.line(traj_canvas, (x0,y0), (x1,y1), (0,255,255), 2)

        # overlay some text
        cv2.putText(overlay, f'Events: {len(xs_pos)+len(xs_neg)} Matches: {num_matches}', (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
        cv2.putText(overlay, f'FPS: {1.0/max(1e-6,(t_now-last_time)):.1f}', (10,60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)

        # show windows
        combined = np.hstack((overlay, heat))
        cv2.imshow('Overlay(matches & pose) | Event Heat', combined)

        cv2.imshow('Trajectory (x vs z, up to scale)', traj_canvas)

        prev_gray = gray.copy()
        last_time = t_now

    # keys
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('p'):
        paused = not paused
    if key == ord('s'):
        saving = not saving
    if key == ord('r'):
        # reset integration
        R_cum = np.eye(3)
        t_cum = np.zeros((3,1))
        traj = []

# cleanup
cap.release()
cv2.destroyAllWindows()
if SAVE_LOG:
    f_log.close()
