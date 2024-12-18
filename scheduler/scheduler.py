import time
import threading


class Scheduler:
    def __init__(self, lcd, boards, notification_manager=None):
        """
        Initializes the scheduler with the given LCD, boards, and notification manager.
        """
        self.lcd = lcd
        self.boards = boards
        self.notification_manager = notification_manager
        self.current_board_index = 0
        self.running = True
        self.thread = None
        self.provider_list: set = self._build_provider_list()

    def _build_provider_list(self) -> set:
        provider_list = set()
        for board in self.boards:
            if board.data_provider is not None:
                provider_list.add(board.data_provider)
        return provider_list

    def _start_providers(self):
        for provider in self.provider_list:
            provider.start()

    def _stop_providers(self):
        for provider in self.provider_list:
            provider.stop()

    def rotate_boards(self):
        """
        Rotates the boards in a loop until the scheduler is stopped. The boards are displayed in the order they are
        provided to the scheduler. If a board has a duration, it will be displayed for that duration before moving to
        the next board. If a board has an update interval, it will be updated every update interval.

        If a notification manager is provided, it will be used to display notifications on top of the boards. The
        notifications will be displayed first and the time taken to display the notification will be added to the end
        time of the current board. The board will be displayed after the notification has been displayed.

        If a board decides to stop displaying, the next board will be displayed immediately.
        """
        while self.running:
            # if any notifications are available, display them first
            if (
                self.notification_manager
                and self.notification_manager.has_notifications()
            ):
                self.notification_manager.display_next_notification(self.lcd, {})

            # get the current board to display
            board = self.boards[self.current_board_index]

            start_time = time.time()
            last_update_time = start_time
            sleep_time = (
                0.1 if board.update_interval > 100 else board.update_interval / 1000
            )
            context = {
                "start_time": start_time,
                "end_time": start_time + board.duration,
            }

            # display the board
            self.lcd.clear()
            continue_board_display = board.display(self.lcd, context)

            # if board has decided to stop displaying, move to the next board
            if not continue_board_display:
                self.current_board_index = (self.current_board_index + 1) % len(
                    self.boards
                )
                continue

            # loop until the board duration has elapsed or the board decides to stop displaying
            # if any notifications are available, display them first and add the time taken to display the notification
            # to the end time of the current board
            while continue_board_display and time.time() < context["end_time"]:
                if not self.running:
                    break

                # if any notifications are available, display them first
                if (
                    self.notification_manager
                    and self.notification_manager.has_notifications()
                ):
                    notification_start_time = time.time()
                    self.notification_manager.display_next_notification(self.lcd, {})
                    self.lcd.clear()

                    # add the time taken to display the notification to the end time of the current board
                    context["end_time"] += time.time() - notification_start_time

                    # if there are more notifications, continue displaying them
                    if self.notification_manager.has_notifications():
                        continue

                    # get the current board to display after the notification
                    continue_board_display = board.display(self.lcd, context)
                    if not continue_board_display:
                        self.current_board_index = (self.current_board_index + 1) % len(
                            self.boards
                        )

                # update the board display every update_interval
                if time.time() - last_update_time > board.update_interval / 1000:
                    last_update_time = time.time()
                    continue_board_display = board.update(self.lcd, context)
                time.sleep(sleep_time)

            # move to the next board
            self.current_board_index = (self.current_board_index + 1) % len(self.boards)

    def start(self):
        """
        Starts the scheduler and rotates the boards in a separate thread.
        """
        self.thread = threading.Thread(target=self.rotate_boards, daemon=True)
        self.thread.start()
        self._start_providers()

    def stop(self):
        """
        Stops the scheduler and joins the thread. Joins immediately if the board displayed is not a notification board.
        If it is a notification board, it will wait until the notification board duration has elapsed.
        """
        self.running = False
        if self.thread:
            self.thread.join()
        self._stop_providers()
        self.lcd.clear()
        self.lcd.backlight_enabled = False
