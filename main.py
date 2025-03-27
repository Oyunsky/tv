# TODO: Add more colors for state and attributes

import curses
from enum import Enum, auto


class WAttribute(Enum):
    FOCUSABLE = auto()
    CLICKABLE = auto()


class WState(Enum):
    FOCUSED   = auto()
    UNFOCUSED = auto()
    CLICKED   = auto()


class WColor:
    FOCUSED   = 1
    CLICKED   = 2
    CLICKABLE = 3


KEY_Q = 113
KEY_R = 114
KEY_H = 104
KEY_J = 106
KEY_K = 107
KEY_L = 108
KEY_ENTER = 10
KEY_SPACE = 32
KEY_TAB = 9


class V2:
    __slots__ = ["y", "x"]

    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __repr__(self):
        return f"y={self.y} x={self.x}"


class Widget:
    __slots__ = ["scr", "_state", "attributes", "y", "x"]

    def __init__(self, scr, y, x, state=None, attributes=None):
        self.scr = scr
        self.y = y
        self.x = x
        self._state = state
        self.attributes = attributes or set()

    def draw(self):
        raise NotImplementedError

    def handle_event(self, key):
        pass

    def has_attribute(self, attribute):
        return attribute in self.attributes

    def set_attribute(self, attribute):
        self.attributes.add(attribute)

    def remove_attribute(self, attribute):
        self.attributes.discard(attribute)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state


class DrawableWidget(Widget):
    def draw(self):
        raise NotImplementedError


class Label(DrawableWidget):
    def __init__(self, scr, y, x, text):
        super().__init__(scr, y, x)
        self.text = text

    def draw(self):
        color = curses.color_pair(WColor.FOCUSED) if self.state == WState.FOCUSED else curses.color_pair(0)
        self.scr.addstr(self.y, self.x, self.text, color)


class Button(DrawableWidget):
    def __init__(self, scr, y, x, text):
        super().__init__(scr, y, x)
        self.text = text
        self.set_attribute(WAttribute.FOCUSABLE)
        self.set_attribute(WAttribute.CLICKABLE)

    def draw(self):
        color = curses.color_pair(WColor.CLICKABLE)
        if self.state == WState.CLICKED:
            color = curses.color_pair(WColor.CLICKED)
        elif self.state == WState.FOCUSED:
            color = curses.color_pair(WColor.FOCUSED)
        self.scr.addstr(self.y, self.x, self.text, color)

    def handle_event(self, key):
        if key in (KEY_ENTER, KEY_SPACE):
            self.state = WState.CLICKED
            self.draw()
            self.scr.refresh()
            curses.napms(500)
            self.state = WState.FOCUSED


class VLayout(Widget):
    __slots__ = ["spacing", "focused_index", "widgets"]

    def __init__(self, scr, y, x, spacing=1):
        super().__init__(scr, y, x)

        self.attributes = {WAttribute.FOCUSABLE}

        self.spacing = spacing
        self.focused_index = -1
        self.widgets = []

    def add_widget(self, widget):
        new_y = self.y + len(self.widgets) * self.spacing
        widget.y = new_y
        widget.x = self.x
        self.widgets.append(widget)

        if self.focused_index == -1 and widget.has_attribute(WAttribute.FOCUSABLE):
            self.focused_index = len(self.widgets) - 1

    def draw(self):
        for widget in self.widgets:
            widget.draw()

    def handle_event(self, key):
        if self.focused_index == -1:
            return

        focused_widget = self.widgets[self.focused_index]
        focused_widget.state = WState.UNFOCUSED

        if key == KEY_J:
            while True:
                self.focused_index = (self.focused_index + 1) % len(self.widgets)
                if self.widgets[self.focused_index].has_attribute(WAttribute.FOCUSABLE):
                    break
        elif key == KEY_K:
            while True:
                self.focused_index = (self.focused_index - 1) % len(self.widgets)
                if self.widgets[self.focused_index].has_attribute(WAttribute.FOCUSABLE):
                    break

        self.widgets[self.focused_index].state = WState.FOCUSED
        self.widgets[self.focused_index].handle_event(key)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
        if state == WState.FOCUSED and self.focused_index != -1:
            self.widgets[self.focused_index].state = WState.FOCUSED
        elif state == WState.UNFOCUSED:
            for widget in self.widgets:
                widget.state = WState.UNFOCUSED


class Renderer:
    __slots__ = ["scr", "event_key", "focused_index", "widgets"]

    def __init__(self, scr):
        self.scr = scr
        self.scr.timeout(0)
        self.event_key = None
        self.focused_index = -1
        self.widgets = []

    def add_widget(self, widget):
        self.widgets.append(widget)
        if self.focused_index == -1 and widget.has_attribute(WAttribute.FOCUSABLE):
            self.focused_index = len(self.widgets) - 1
            widget.state = WState.FOCUSED

    def draw_widgets(self):
        self.scr.erase()
        for widget in self.widgets:
            widget.draw()
        self.scr.refresh()

    def update(self):
        self.event_key = self.scr.getch()

        if self.event_key == KEY_TAB:
            self.widgets[self.focused_index].state = WState.UNFOCUSED
            for _ in range(len(self.widgets)):
                self.focused_index = (self.focused_index + 1) % len(self.widgets)
                if self.widgets[self.focused_index].has_attribute(WAttribute.FOCUSABLE):
                    self.widgets[self.focused_index].state = WState.FOCUSED
                    break

        if self.widgets:
            self.widgets[self.focused_index].handle_event(self.event_key)

        self.draw_widgets()

    def should_close(self):
        return self.event_key == KEY_Q

    @property
    def size(self):
        return V2(*self.scr.getmaxyx())


def main(scr):
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(WColor.FOCUSED, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(WColor.CLICKED, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(WColor.CLICKABLE, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    r = Renderer(scr)
    r.add_widget(Label(scr, 0, 0, "[Widget Button]"))
    r.add_widget(Button(scr, 1, 0, "Button 1"))

    l = VLayout(scr, 5, 0)
    l.add_widget(Label(scr, 0, 0, "[Widget VLayout]"))
    l.add_widget(Button(scr, 0, 0, "SubButton 1"))
    l.add_widget(Button(scr, 0, 0, "SubButton 2"))
    l.add_widget(Button(scr, 0, 0, "SubButton 3"))

    r.add_widget(l)

    while not r.should_close():
        r.update()


if __name__ == "__main__":
    curses.wrapper(main)
