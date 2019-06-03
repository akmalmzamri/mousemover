import datetime
import random
import sys
import threading
import time
import win32api
import win32con

SCREEN_WIDTH = win32api.GetSystemMetrics(0)
SCREEN_HEIGHT = win32api.GetSystemMetrics(1)

class Mouse_Handler:

    def __init__(self):
        # thread
        self.active_thread = None
        self.timer_handler_thread = None

        # event
        self.timer_countdown = None
        self.movement_delay = None

    def move_mouse(self, ui_input):
        delay = ui_input.delay
        offset = ui_input.offset
        random_movement_enabled = ui_input.random_movement_enabled
        random_delay_enabled = ui_input.random_delay_enabled
        random_movement = ui_input.random_movement
        random_delay = ui_input.random_delay

        random_x_movement_modifier = 0
        random_y_movement_modifier = 0
        random_delay_modifier = 0
        random_x_direction = 1
        random_y_direction = 1

        """
        Move mouse <offset> away relative to the current position every <delay> seconds.
        65535 is used to normalize absolute coordinates so we can get the same mouse movement 
        regardless of screen size (0,0) to (65535,65535)
        """
        while not self.movement_delay.is_set():
            # Check if random movement is enabled
            if random_movement_enabled:
                random_x_movement_modifier = random.randint(int(random_movement[0]), int(random_movement[1]))
                random_y_movement_modifier = random.randint(int(random_movement[0]), int(random_movement[1]))
                random_x_direction = 1 if random.random() < 0.5 else -1
                random_y_direction = 1 if random.random() < 0.5 else -1

            # Check if random delay is enabled
            if random_delay_enabled:
                random_delay_modifier = random.randint(int(random_delay[0]), int(random_delay[1]))

            # Perform the first movement
            x, y = win32api.GetCursorPos()
            win32api.mouse_event(
                    win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, 
                    int((x / SCREEN_WIDTH * 65535.0) + ((offset + random_x_movement_modifier) * random_x_direction)),
                    int((y / SCREEN_HEIGHT * 65535.0) + ((offset + random_x_movement_modifier) * random_y_direction))
                )
            self.movement_delay.wait(delay + random_delay_modifier)
            
            # Perform the second movement
            x, y = win32api.GetCursorPos()
            win32api.mouse_event(
                    win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, 
                    int((x / SCREEN_WIDTH * 65535.0) - ((offset + random_x_movement_modifier) * random_x_direction)),
                    int((y / SCREEN_HEIGHT * 65535.0) - ((offset + random_x_movement_modifier) * random_y_direction))
                )
            self.movement_delay.wait(delay + random_delay_modifier)
    
    def start_mouse_movement(self, ui_input):
        self.movement_delay = threading.Event()
        mouse_movement_thread = threading.Thread(target=self.move_mouse, args=(ui_input,))
        self.active_thread = mouse_movement_thread
        mouse_movement_thread.start()
    
    def stop_mouse_movement(self):
        if self.movement_delay is not None:
            self.movement_delay.set()
        
        if self.active_thread is not None:
            self.active_thread.join()
        
        if self.timer_countdown is not None:
            self.timer_countdown.set()
    
    def start_timer(self, timer, ui):
        self.timer_handler_thread = threading.Thread(target=self.timer_handler, args=(timer, ui,))
        self.timer_handler_thread.start()
        self.display_timer_thread = threading.Thread(target=self.display_timer, args=(timer, ui,))
        self.display_timer_thread.start()
    
    def display_timer(self, timer, ui):
        timer_start_time = time.time()
        time_elapsed = 0
        self.timer_countdown = threading.Event()
        
        while time_elapsed <= timer and not self.timer_countdown.is_set():
            # Update timer display in UI
            timer_current_time = time.time()
            time_elapsed = int(timer_current_time - timer_start_time)
            time_left = timer - time_elapsed
            ui.ui.currentTimerValue.setText(str(datetime.timedelta(seconds=time_left)))

    def timer_handler(self, timer, ui):
        self.active_thread.join(timer)
        self.movement_delay.set()
        self.active_thread.join()
        ui.stop_mouse_movement()