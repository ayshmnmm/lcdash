import time
from boards.board import Board
from notifications.notifier import Notifier
from icons.manager import IconManager
import icons.icons as icons


class MotionDetectionNotification(Board):
    def display(self, lcd, context):
        print("MotionDetectionNotification got context", context)
        lcd.clear()
        lcd.write_string(
            f"{IconManager.use_icon(lcd, icons.BELL)} {context['event']['message']}"
        )
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


class MotionDetectionNotifier(Notifier):
    def __init__(self, notification_manager, notification_board, data_provider=None):
        super().__init__(notification_manager, notification_board, data_provider)
        data_provider.subscribe(self.handle_event)

    def handle_event(self, event):
        print(f"Received event")
        event["message"] = f"Motion detected"
        if event["eventType"] != "videoloss":
            self.notify(event, priority=1, duration=30)
