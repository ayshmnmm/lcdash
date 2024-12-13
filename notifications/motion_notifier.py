import time
from boards.board import Board

class MotionDetectionNotification(Board):
    def display(self, lcd, context):
        lcd.clear()
        lcd.write_string(f"{context['event']['message']}")
        self.msg_start_time = time.time()
        self.last_update_time = self.msg_start_time
        return True

    def update(self, lcd, context):
        lcd.cursor_pos = (1, 0)
        lcd.write_string(f"Time: {time.time() - self.msg_start_time:.2f}s")
        fps = 1 / (time.time() - self.last_update_time)
        lcd.cursor_pos = (2, 0)
        lcd.write_string(f"FPS: {fps:.2f}")
        self.last_update_time = time.time()
        return True
    
class MotionDetectionNotifier():
    def __init__(self, notification_manager):
        self.notification_manager = notification_manager
        self.motion_detection_notification = MotionDetectionNotification(duration=3, update_interval=50)

    def notify(self, event):
        self.notification_manager.add_notification(self.motion_detection_notification, event)
        