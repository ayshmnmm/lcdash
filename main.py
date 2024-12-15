import time
from RPLCD.i2c import CharLCD
from os import getenv
from dotenv import load_dotenv

from boards.clock_board import ClockBoard
from boards.greeting_board import GreetingBoard

from data_providers.clock_provider import ClockProvider
from data_providers.motion_events_provider import MotionEventsProvider

from scheduler.scheduler import Scheduler

from notifications.manager import NotificationManager
from notifications.motion_notifier import (
    MotionDetectionNotifier,
    MotionDetectionNotification,
)


if __name__ == "__main__":
    load_dotenv()

    lcd = CharLCD(
        i2c_expander="PCF8574", address=0x27, port=1, cols=20, rows=4, dotsize=8
    )

    boards = (
        ClockBoard(duration=5, data_provider=ClockProvider(update_interval=1)),
        GreetingBoard(update_interval=75),
    )

    notification_manager = NotificationManager()

    # Motion detection
    motion_provider = MotionEventsProvider(
        url=getenv("ISAPI_EVENT_URL"),
        username=getenv("ISAPI_USERNAME"),
        password=getenv("ISAPI_PASSWORD"),
    )
    motion_notifier = MotionDetectionNotifier(
        notification_manager,
        MotionDetectionNotification(duration=3, update_interval=200),
        motion_provider,
    )
    motion_provider.start()  # start listening on the event stream

    scheduler = Scheduler(lcd, boards, notification_manager)
    scheduler.start()

    time.sleep(6)
    print("Adding motion detection notification")
    # motion_notifier.notify({"message": "#noti 1"})
    time.sleep(5)
    print("Adding another motion detection notification")
    motion_notifier.notify({"message": "#noti 2"}, duration=10)
    time.sleep(10)
    print("Adding another 3rd motion detection notification")
    # motion_notifier.notify({"message": "#noti 3"})

    print("Press Ctrl+C to stop the scheduler")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()
        print("Scheduler stopped")
