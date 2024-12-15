class Notifier:
    """
    Base class for all notifiers.
    """

    def __init__(self, notification_manager, notification_board, data_provider=None):
        """
        Initializes the notifier with the given notification manager, notification board, and data provider.
        """
        self.notification_manager = notification_manager
        self.notification_board = notification_board
        self.data_provider = data_provider

    def notify(self, event, priority: int = 5, duration=None):
        """
        Add the notification to the notification manager queue.
        """
        self.notification_manager.add_notification(self.notification_board, event, priority, duration)
