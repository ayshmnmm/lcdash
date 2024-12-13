import time
import threading

class Scheduler:
    def __init__(self, lcd, boards, notification_manager = None):
        self.lcd = lcd
        self.boards = boards
        self.notification_manager = notification_manager
        self.current_board_index = 0
        self.running = True
        self.thread = None
        self.provider_list = self._build_provider_list()

    def _build_provider_list(self):
        provider_list = []
        for board in self.boards:
            if board.data_provider is not None:
                provider_list.append(board.data_provider)
        return provider_list
    
    def start_providers(self):
        for provider in self.provider_list:
            provider.start()

    def stop_providers(self):
        for provider in self.provider_list:
            provider.stop()

    def rotate_boards(self):
        while self.running:
            board = self.boards[self.current_board_index]

            start_time = time.time()
            last_update_time = start_time
            sleep_time = 0.1 if board.update_interval > 100 else board.update_interval / 1000
            context = {'start_time': start_time, 'end_time': start_time + board.duration}

            self.lcd.clear()
            continue_board_display = board.display(self.lcd, context)

            if not continue_board_display:
                self.current_board_index = (self.current_board_index + 1) % len(self.boards)
                continue

            while continue_board_display and time.time() < context['end_time']:
                if time.time() - last_update_time > board.update_interval / 1000:
                    last_update_time = time.time()
                    continue_board_display = board.update(self.lcd, context)
                time.sleep(sleep_time)

            self.current_board_index = (self.current_board_index + 1) % len(self.boards)

    def start(self):
        self.thread = threading.Thread(target=self.rotate_boards, daemon=True)
        self.thread.start()
        self.start_providers()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self.stop_providers()
        self.lcd.clear()
        self.lcd.backlight_enabled = False
