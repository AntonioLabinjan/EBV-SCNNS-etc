'''
1. **Original window**

   * Prikazuje normalni frame iz kamere ili videa.
   * Nema nijednu obradu, samo “što kamera vidi”.
   * Koristi se kao referenca za event i flow vizualizacije.

2. **Crni background s šarenim flekama (optical flow)**

   * Računa pomak svakog pixela između frameova (dx, dy).
   * Boja = smjer pokreta, svjetlina = brzina (magnitude).
   * Vizualizira **kako se objekti kreću** i **smjer** pokreta.

3. **Plava pozadina s crvenim linijama (event map / thresholded difference)**

   * Prikazuje pixele koji su se promijenili više od thresholda.
   * Crvene linije = mjesta gdje se dogodio pokret (event).
   * Simulira **event-based kameru** i detektira “hot spots” aktivnosti.
'''

import cv2
import numpy as np
import time
import csv

# PARAMETERS
THRESHOLD = 25
DISPLAY_SCALE = 1
LOG_EVENTS = True
VIDEO_SOURCE = 0  # 0 = laptop camera, ili putanja videa

# Initialize capture
cap = cv2.VideoCapture(VIDEO_SOURCE)
ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

# Optical flow parameters
flow_params = dict(pyr_scale=0.5, levels=3, winsize=15,
                   iterations=3, poly_n=5, poly_sigma=1.2, flags=0)

# Event log
if LOG_EVENTS:
    csv_file = open('event_log.csv', mode='w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['timestamp', 'x', 'y', 'polarity'])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Event generation
    diff = cv2.absdiff(gray, prev_gray)
    events = np.zeros_like(diff)
    events[diff > THRESHOLD] = 255
    
    # Polarity (brighten/darken)
    polarity = np.sign(gray.astype(np.int16) - prev_gray.astype(np.int16))
    
    timestamp = time.time()
    if LOG_EVENTS:
        ys, xs = np.where(events>0)
        for x, y in zip(xs, ys):
            csv_writer.writerow([timestamp, x, y, polarity[y,x]])

    # Optical flow
    flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, **flow_params)
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    
    # Overlay flow vectors
    hsv = np.zeros_like(frame)
    hsv[...,1] = 255
    hsv[...,0] = ang * 180 / np.pi / 2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    flow_rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    # Event density heatmap
    heatmap = cv2.applyColorMap(events, cv2.COLORMAP_JET)
    
    # Combine original frame, flow, heatmap
    combined = np.hstack((frame, flow_rgb, heatmap))
    combined = cv2.resize(combined, (combined.shape[1]*DISPLAY_SCALE, combined.shape[0]*DISPLAY_SCALE))
    
    # Count events
    num_events = np.sum(events>0)
    cv2.putText(combined, f'Events: {num_events}', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    
    cv2.imshow("Event-based Drone Simulator", combined)
    
    prev_gray = gray.copy()
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if LOG_EVENTS:
    csv_file.close()
