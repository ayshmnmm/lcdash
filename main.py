from RPLCD.i2c import CharLCD

from boards.clock_board import ClockBoard
from boards.greeting_board import GreetingBoard

from data_providers.clock_provider import ClockProvider

from scheduler.scheduler import Scheduler


if __name__ == '__main__':
    lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=4, dotsize=8)

    boards = (
              ClockBoard(duration=5, data_provider=ClockProvider(update_interval=1)),
              GreetingBoard(update_interval=10)
    )
    
    
    scheduler = Scheduler(lcd, boards)
    scheduler.start()

    print("Press Ctrl+C to stop the scheduler")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        scheduler.stop()
        print("Scheduler stopped")
