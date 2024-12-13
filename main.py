import time
from RPLCD.i2c import CharLCD

from boards.clock_board import ClockBoard
from boards.greeting_board import GreetingBoard

from data_providers.clock_provider import ClockProvider

from scheduler.scheduler import Scheduler

from notifications.manager import NotificationManager
from notifications.motion_notifier import MotionDetectionNotifier


if __name__ == '__main__':
    lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=4, dotsize=8)

    boards = (
              ClockBoard(duration=2, data_provider=ClockProvider(update_interval=1)),
              GreetingBoard(update_interval=75)
    )

    notification_manager = NotificationManager()
    
    motion_notifier = MotionDetectionNotifier(notification_manager)

    scheduler = Scheduler(lcd, boards, notification_manager)
    scheduler.start()

    time.sleep(3)
    print("Adding motion detection notification")
    motion_notifier.notify({'message': "Notification num 1"})
    time.sleep(5)
    print("Adding another motion detection notification")
    motion_notifier.notify({'message': "Notification num 2"})
    time.sleep(2)
    print("Adding another 3rd motion detection notification")
    motion_notifier.notify({'message': "Notification num 3"})
   
    print("Press Ctrl+C to stop the scheduler")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()
        print("Scheduler stopped")
