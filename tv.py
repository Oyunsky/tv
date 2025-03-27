import curses


class VState:
    IDLE = 0
    FOCUSED = 1
    CLICKED = 2


class VAttribute:
    FOCUSABLE = 0
    CLICKABLE = 1


class VColor:
    DEFAULT = 0
    FOCUSED = 1
    CLICKED = 2


class VApplication:
    __slots__ = ("scr", "event_key", "widgets", "focused_widget")

    def __init__(self):
        self.scr = curses.initscr()
        self.scr.timeout(0)
        self._init_colors()

        self.event_key = None

        self.widgets = []
        self.focused_widget = -1

    def _init_colors(self):
        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    def add_widget(self, widget):
        self.widgets.append(widget)

        if self.focused_widget == -1 and widget.has_attr(VAttribute.FOCUSABLE):
            widget.state = VState.FOCUSED
            self.focused_widget = len(self.widgets) - 1

    def draw_widgets(self):
        self.scr.erase()

        for widget in self.widgets:
            widget.draw()

        self.scr.refresh()

    def update(self):
        self.event_key = self.scr.getch()

        if self.event_key == ord('\t'):
            self.widgets[self.focused_widget].state = VState.IDLE
            for _ in range(len(self.widgets)):
                self.focused_widget = (self.focused_widget + 1) % len(self.widgets)
                if self.widgets[self.focused_widget].has_attr(VAttribute.FOCUSABLE):
                    self.widgets[self.focused_widget].state = VState.FOCUSED
                    break

        if self.widgets:
            self.widgets[self.focused_widget].event(self.event_key)

        self.draw_widgets()

    def should_close(self):
        return self.event_key == ord('q')


class VBaseWidget:
    __slots__ = ("app", "scr", "state", "attributes")

    def __init__(self, app):
        self.app = app
        self.scr = app.scr

        self.state = VState.IDLE
        self.attributes = set()

    def draw(self): ...

    def update(self): ...

    def event(self, key): ...

    def has_attr(self, attr):
        return attr in self.attributes


class VLabel(VBaseWidget):
    __slots__ = ("y", "x", "text")

    def __init__(self, app, y, x, text):
        super().__init__(app)

        self.y = y
        self.x = x
        self.text = text

    def draw(self):
        self.scr.addstr(self.y, self.x, self.text)


class VButton(VLabel):
    def __init__(self, app, y, x, text):
        super().__init__(app, y, x, text)

        self.attributes.add(VAttribute.FOCUSABLE)
        self.attributes.add(VAttribute.CLICKABLE)

    def draw(self):
        color = (
            VColor.CLICKED if self.state == VState.CLICKED else
            VColor.FOCUSED if self.state == VState.FOCUSED else VColor.DEFAULT
        )
        self.scr.addstr(self.y, self.x, self.text, curses.color_pair(color))

    def event(self, key):
        if key in (ord('\n'), ord(' ')):
            self.state = VState.CLICKED
            self.draw()
            self.scr.refresh()
            curses.napms(500)
            self.state = VState.FOCUSED


def main():
    app = VApplication()
    app.add_widget(VLabel(app, 0, 0, "[Hello, World]"))
    app.add_widget(VButton(app, 1, 0, "Button 1"))
    app.add_widget(VButton(app, 2, 0, "Button 2"))

    while not app.should_close():
        app.update()


if __name__ == "__main__":
    main()
