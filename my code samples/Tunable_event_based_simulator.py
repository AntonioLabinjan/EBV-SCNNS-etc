import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading
import time

class EventBasedSimulator:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.prev_gray = None
        self.threshold = 25
        self.event_count = 0
        self.running = True

        self.root = tk.Tk()
        self.root.title("Event-Based Vision Simulator")

        self.slider = ttk.Scale(self.root, from_=5, to=100, orient="horizontal", command=self.update_threshold)
        self.slider.set(self.threshold)
        self.slider.pack(pady=5)

        self.label = ttk.Label(self.root, text=f"Threshold: {self.threshold}")
        self.label.pack()

        self.count_label = ttk.Label(self.root, text=f"Events: 0")
        self.count_label.pack(pady=5)

        threading.Thread(target=self.camera_loop, daemon=True).start()
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self.root.mainloop()

    def update_threshold(self, val):
        self.threshold = int(float(val))
        self.label.config(text=f"Threshold: {self.threshold}")

    def camera_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if self.prev_gray is None:
                self.prev_gray = gray
                continue

            diff = cv2.absdiff(gray, self.prev_gray)
            events = (diff > self.threshold).astype(np.uint8)
            pos_events = np.where(gray > self.prev_gray + self.threshold, 1, 0).astype(np.uint8)
            neg_events = np.where(gray < self.prev_gray - self.threshold, 1, 0).astype(np.uint8)

            pos_vis = np.zeros_like(frame)
            neg_vis = np.zeros_like(frame)
            pos_vis[pos_events == 1] = [0, 0, 255]  # red for positive
            neg_vis[neg_events == 1] = [255, 0, 0]  # blue for negative

            overlay = cv2.addWeighted(frame, 0.5, pos_vis + neg_vis, 1.0, 0)

            self.event_count += np.count_nonzero(events)
            self.count_label.config(text=f"Events: {self.event_count}")

            cv2.imshow("Event-Based Overlay", overlay)
            self.prev_gray = gray

            if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
                self.stop()
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    EventBasedSimulator()
