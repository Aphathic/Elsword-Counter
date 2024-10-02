import customtkinter as ctk
import keyboard  # Module for capturing global key presses

# Made by Nyno3333, Improved by Shiroah

# Class to handle each individual timer
class Timer:
    def __init__(self, name, duration, label):
        self.name = name
        self.duration = duration
        self.remaining_time = duration
        self.label = label
        self.running = False
        self.timer_id = None  # To store the after() callback ID

    # Start the timer using the after() method
    def start(self):
        self.running = True
        self._countdown()

    # Countdown function that uses the after() method
    def _countdown(self):
        if self.running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_label(f"{self.name} Time Left: {self.remaining_time} sec", "#ff0000")  # Red text while running
            self.timer_id = self.label.after(1000, self._countdown)
        elif self.remaining_time <= 0:
            self.update_label(f"{self.name} Time's up!", "#5fce4e")
            self.running = False  # Stop the timer when time's up

    # Update the label text and color
    def update_label(self, text, color):
        self.label.configure(text=text, text_color=color)

    # Reset the timer to its initial state
    def reset(self):
        if self.name != "Freed Shadow" or self.remaining_time <= 0:
            if self.timer_id:
                self.label.after_cancel(self.timer_id)
            self.remaining_time = self.duration
            self.update_label(f"{self.name} Time Left: {self.duration} sec", "#ff0000")  # Red text after reset
            self.running = True
            self._countdown()

    # Stop the timer
    def stop(self):
        if self.timer_id:
            self.label.after_cancel(self.timer_id)
        self.running = False

# Function to handle key presses
def handle_keypress(timer_name):
    if timer_name in timers:
        timers[timer_name].reset()

# Main application setup
def main():
    # Configuration of initial timer values and key bindings
    timer_settings = {
        "Aura": {"duration": 31, "key": "q"},
        "ID": {"duration": 18, "key": "r"},
        "Amorphous": {"duration": 4, "key": "s"},
        "infernal Hands": {"duration": 6, "key": "c"},
        "blanket": {"duration": 6, "key": "f"},
        "freeze" : {"duration": 31, "key": "d"}
    }

    # Create the main application window
    app = ctk.CTk()
    app.title("Demersio")
    app.geometry("250x250")  # Window size
    app.attributes('-topmost', True)  # Keep the window on top
    app.attributes('-alpha', 1.0)  # Make window fully visible
    app.resizable(False, False)  # Prevent window resizing
    app.configure(fg_color="#000000")

    # Configure customtkinter appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Dictionary to hold timer objects
    global timers  # Make timers accessible in handle_keypress
    timers = {}

    # Create labels and initialize Timer objects for each timer setting
    for name, config in timer_settings.items():
        label = ctk.CTkLabel(
            app, 
            text=f"{name} Time Left: 0 sec", 
            font=("Helvetica", 18), 
            text_color="#ff0000",  # Default red text
            anchor="center"
        )
        label.pack(pady=5)

        # Initialize the timer object
        timer = Timer(name, config["duration"], label)
        timers[name] = timer

        # Immediately set remaining time to 0 and display "Time's up!" initially
        timer.remaining_time = 0
        timer.update_label(f"{timer.name} Time's up!", "#5fce4e")

    # Function to check if a key press is not an arrow key
    def key_listener(event):
        if event.name not in ['up', 'down', 'left', 'right']:  # Ignore arrow keys
            for name, config in timer_settings.items():
                if event.name == config["key"]:
                    handle_keypress(name)

    # Register key listener
    keyboard.hook(key_listener)

    # Run the main loop of the application
    app.mainloop()

    # Stop all timers when the application closes
    for timer in timers.values():
        timer.stop()

if __name__ == "__main__":
    main()