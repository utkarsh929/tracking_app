import pyautogui
import time
import os
import threading
from pynput import keyboard, mouse
from tkinter import Tk, Label, Button, Entry, StringVar, messagebox, Frame, Canvas
import tkinter.font as tkFont

# Global variables
is_tracking = False
interval = 10
count = 0
key_count = 0
mouse_click_count = 0
screenshot_thread = None

# Directory for saving screenshots
os.makedirs('screenshots', exist_ok=True)

def take_screenshot():
    """Function to take screenshots at specified intervals."""
    global count
    while is_tracking:
        count += 1
        screenshot = pyautogui.screenshot()
        screenshot.save(f'screenshots/screenshot_{count}.png')
        print(f'Screenshot {count} taken.')
        time.sleep(interval)

def start_tracking():
    """Function to start tracking user activity and screenshots."""
    global is_tracking, screenshot_thread, key_count, mouse_click_count
    if is_tracking:
        return  # Already tracking

    is_tracking = True
    key_count = 0
    mouse_click_count = 0

    # Start screenshot thread if not already started
    if screenshot_thread is None or not screenshot_thread.is_alive():
        screenshot_thread = threading.Thread(target=take_screenshot)
        screenshot_thread.start()

    # Start keyboard and mouse listeners
    keyboard.Listener(on_press=on_key_press).start()
    mouse.Listener(on_click=on_click).start()

    print("Tracking started.")
    app.update_status("Tracking started...")

def stop_tracking():
    """Function to stop tracking user activity and screenshots."""
    global is_tracking
    is_tracking = False
    print(f"Tracking stopped. Total key presses: {key_count}, Mouse clicks: {mouse_click_count}")
    app.update_status(f"Tracking stopped. Key presses: {key_count}, Mouse clicks: {mouse_click_count}")

def on_key_press(key):
    """Function to log key presses."""
    global key_count
    key_count += 1

def on_click(x, y, button, pressed):
    """Function to log mouse clicks."""
    global mouse_click_count
    if pressed:
        mouse_click_count += 1

def update_interval(new_interval):
    """Function to update the screenshot interval."""
    global interval
    try:
        interval = float(new_interval)
        print(f"Interval updated to {interval} seconds.")
        app.update_status(f"Interval updated to {interval} seconds.")
    except ValueError:
        print("Invalid interval value. Please enter a number.")
        messagebox.showerror("Invalid Input", "Please enter a valid number for the interval.")

def draw_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """Draw a rounded rectangle on a canvas."""
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return canvas.create_polygon(points, smooth=True, **kwargs)

# GUI class for the application
class TimeTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("Time Tracker")

        # Set bold font
        self.bold_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

        # Create a canvas with a solid pale blue background
        self.canvas = Canvas(master, width=1500, height=900, bg="#add8e6")  
        self.canvas.pack(fill="both", expand=True)

        # Full screen mode
        self.master.attributes('-fullscreen', True)

        # Larger Rounded Frame for Interval Input
        self.interval_frame_bg = draw_rounded_rectangle(self.canvas, 300, 100, 1200, 300, radius=20, fill='#FFFFE0', outline='#FFFFE0')  
        self.interval_frame = Frame(self.canvas, bg='#FFFFE0')
        self.canvas.create_window(750, 200, window=self.interval_frame)

        self.label = Label(self.interval_frame, text="Interval between screenshots (seconds):", font=self.bold_font, bg='#FFFFE0')
        self.label.pack(side='left', padx=5)

        self.interval_var = StringVar(value=str(interval))
        self.interval_entry = Entry(self.interval_frame, textvariable=self.interval_var, width=10, font=self.bold_font)
        self.interval_entry.pack(side='left', padx=5)

        # Larger Rounded Frame for Control Buttons
        self.control_frame_bg = draw_rounded_rectangle(self.canvas, 300, 350, 1200, 550, radius=20, fill='#FFFFE0', outline='#FFFFE0')  # Yellow background
        self.control_frame = Frame(self.canvas, bg='#FFFFE0')
        self.canvas.create_window(750, 450, window=self.control_frame)

        self.start_button = Button(self.control_frame, text="Start Tracking", command=self.start_tracking, font=self.bold_font, width=15)
        self.start_button.pack(side='left', padx=10)

        self.stop_button = Button(self.control_frame, text="Stop Tracking", command=self.stop_tracking, font=self.bold_font, width=15)
        self.stop_button.pack(side='left', padx=10)

        self.update_button = Button(self.control_frame, text="Update Interval", command=self.update_interval, font=self.bold_font, width=15)
        self.update_button.pack(side='left', padx=10)

        # Larger Rounded Frame for Status Bar
        self.status_frame_bg = draw_rounded_rectangle(self.canvas, 300, 600, 1200, 700, radius=20, fill='#FFFFE0', outline='#FFFFE0')  
        self.status_frame = Frame(self.canvas, bg='#FFFFE0')
        self.canvas.create_window(750, 650, window=self.status_frame)

        self.status_label = Label(self.status_frame, text="Ready", font=self.bold_font, anchor="w", bg='#FFFFE0')
        self.status_label.pack(fill='x', padx=10)

    def start_tracking(self):
        """Button callback to start tracking."""
        try:
            interval = float(self.interval_var.get())
            update_interval(interval)
            start_tracking()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the interval.")

    def stop_tracking(self):
        """Button callback to stop tracking."""
        stop_tracking()

    def update_interval(self):
        """Button callback to update the screenshot interval."""
        new_interval = self.interval_var.get()
        update_interval(new_interval)

    def update_status(self, message):
        """Function to update the status label with a message."""
        self.status_label.config(text=message)

# Main function to run the application
def main():
    global app
    root = Tk()
    app = TimeTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
