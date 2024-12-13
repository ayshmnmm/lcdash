from queue import Queue


class IconManager:
    max_icons = 8
    icon_queue = Queue(maxsize=max_icons)
    icon_slots = {}  # {icon: slot}

    @staticmethod
    def use_icon(lcd, icon_bitmap):
        # if icon is already available, return the slot
        if icon_bitmap in IconManager.icon_slots:
            return IconManager.icon_slots[icon_bitmap]
        else:
            # if there are no available slots, dequeue the oldest icon
            if IconManager.icon_queue.full():
                oldest_icon = IconManager.icon_queue.get()
                available_slot = IconManager.icon_slots.pop(oldest_icon)
            else:
                # available slot is a hex escape sequence like '\x00' to '\x07'
                available_slot = chr(0x00 + len(IconManager.icon_slots))

            # create the custom character on the LCD
            lcd.create_char(ord(available_slot), icon_bitmap)
            IconManager.icon_queue.put(icon_bitmap)
            IconManager.icon_slots[icon_bitmap] = available_slot
            return available_slot
