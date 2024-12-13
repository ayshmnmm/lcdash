import queue
import threading
import time

class NotificationItem:
    def __init__(self, notification_board, event: dict, priority: int = 5):
        self.notification_board = notification_board
        self.event = event
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority
    

class NotificationManager:
    def __init__(self):
        """
        Initializes the NotificationManager with the given list of notifier objects
        """
        self.notification_queue = queue.PriorityQueue()
        self.lock = threading.Lock()

    def add_notification(self, notification_board, event: dict, priority: int = 5):
        """
        Adds a notification to the notification queue with the given priority. Lower priority values will be processed
        first.

        :param notification_board: The notification board that will be used to display the notification
        :param event: The event data that will be displayed by the notification board
        :param priority: The priority of the notification (default: 5)
        """
        with self.lock:
            print(f"Adding notification with priority {priority}")
            self.notification_queue.put(NotificationItem(notification_board, event, priority))

    def get_notification(self):
        """
        Gets the top notification from the notification queue. This method will return None if there are no
        notifications in the queue.

        :return: A tuple containing the notification board and event data or None if there are no notifications
        """
        with self.lock:
            if not self.notification_queue.empty():
                item = self.notification_queue.get()
                return item.notification_board, item.event
            return None
        
    def has_notifications(self):
        """
        Checks if there are any notifications in the queue.

        :return: True if there are notifications in the queue, False otherwise
        """
        with self.lock:
            return not self.notification_queue.empty()
        
    def display_next_notification(self, lcd, context):
        """
        Displays the next notification in the queue on the given LCD.

        :param lcd: The LCD object on which the notification will be displayed
        """
        notification = self.get_notification()
        if notification:
            board, event = notification

            start_time = time.time()
            last_update_time = start_time
            sleep_time = 0.1 if board.update_interval > 100 else board.update_interval / 1000
            context = {'start_time': start_time, 'end_time': start_time + board.duration}
            context["event"] = event.copy()

            lcd.clear()
            continue_board_display = board.display(lcd, context)
            if not continue_board_display:
                return
            
            while continue_board_display and time.time() < context['end_time']:
                if time.time() - last_update_time > board.update_interval / 1000:
                    last_update_time = time.time()
                    continue_board_display = board.update(lcd, context)
                time.sleep(sleep_time)
                