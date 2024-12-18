class Queue:
    """
    A simple queue implementation using a list.
    """

    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.queue = []

    def put(self, item):
        if len(self.queue) < self.maxsize:
            self.queue.append(item)
        else:
            self.queue.pop(0)
            self.queue.append(item)

    def get(self):
        return self.queue.pop(0)

    def empty(self):
        return len(self.queue) == 0

    def full(self):
        return len(self.queue) == self.maxsize

    def remove(self, item):
        if item in self.queue:
            self.queue.remove(item)


class IconManager:
    """
    A class to manage custom icons on the LCD. It keeps track of the icons that are currently available on the LCD and
    the slots they occupy. It also provides a method to use an icon on the LCD.
    """

    max_icons = 8
    icon_queue = Queue(maxsize=max_icons)
    icon_slots = {}  # {icon: slot}

    @staticmethod
    def use_icon(lcd, icon_bitmap):
        """
        Returns the slot of the icon on the LCD. If the icon is not already available on the LCD, it creates a custom
        character for the icon and returns the slot.
        """
        # if icon is already available, return the slot
        if icon_bitmap in IconManager.icon_slots:
            return IconManager.icon_slots[icon_bitmap]
        else:
            # if there are no available slots, dequeue the oldest icon
            available_slot = None
            if IconManager.icon_queue.full():
                oldest_icon = IconManager.icon_queue.get()
                # while oldest_icon not in IconManager.icon_slots and not IconManager.icon_queue.empty():
                #     oldest_icon = IconManager.icon_queue.get()
                if oldest_icon in IconManager.icon_slots:
                    available_slot = IconManager.icon_slots.pop(oldest_icon)
            if available_slot is None:
                for i in range(8):
                    if chr(0x00 + i) not in IconManager.icon_slots.values():
                        available_slot = chr(0x00 + i)
                        break

            # create the custom character on the LCD
            lcd.create_char(ord(available_slot), icon_bitmap)
            IconManager.icon_queue.put(icon_bitmap)
            IconManager.icon_slots[icon_bitmap] = available_slot
            return available_slot

    @staticmethod
    def clear_icon(icon_bitmap):
        """
        Remove icon from the slot and queue.
        """
        if icon_bitmap in IconManager.icon_slots:
            IconManager.icon_slots.pop(icon_bitmap)
            IconManager.icon_queue.remove(icon_bitmap)
            return True
        return False
