import curses
from abc import ABC, abstractmethod


class LeftPanel:
    DEFAULT_COLS = 26

    def __init__(self, stdscr):
        self._stdscr = stdscr

        self.items = [
            ("Профиль", None),
            ("Все обсуждения", 0),
            ("Мои темы", 1),
            ("Прочитанные темы", 2),
            ("Закладки", 3),
            ("Отложенные темы", 4),
            ("Основная категория", None),
            ("Халява", 5),
            ("Торговля", 6),
            ("Работа и услуги", 7),
            ("Арбитраж", 8),
        ]
        self.selected_item = 1

        self.subscr = stdscr.subwin(0, 0, 0, 0)
        self.subscr_cols = self.DEFAULT_COLS

    def render(self):
        if self.subscr_cols > root_scr_x:
            self.subscr_cols = root_scr_x
        elif self.subscr_cols < root_scr_x and self.subscr_cols < self.DEFAULT_COLS:
            self.subscr_cols = min(self.DEFAULT_COLS, root_scr_x)

        self.subscr.resize(root_scr_y, self.subscr_cols)
        self.subscr.box()

        y, x = 1, 3

        for i, (item_name, item_id) in enumerate(self.items):
            color = 1 if i == self.selected_item else 0
            if item_id is None:
                if i > 0:
                    y += 1
                self.subscr.addstr(y, x, f"[{item_name}]", curses.color_pair(color))
                y += 1
            else:
                text = item_name.ljust(18)
                self.subscr.addstr(y, x, f"- {text}", curses.color_pair(color))
                y += 1

    def render_and_refresh(self):
        self.render()
        self.subscr.refresh()

    def resize(self):
        self.subscr.erase()
        self.render_and_refresh()

    def event(self, key):
        if key == ord('k'):
            while True:
                self.selected_item = (self.selected_item - 1) % len(self.items)
                if self.items[self.selected_item][1] is not None:
                    break
            self.render_and_refresh()
        elif key == ord('j'):
            while True:
                self.selected_item = (self.selected_item + 1) % len(self.items)
                if self.items[self.selected_item][1] is not None:
                    break
            self.render_and_refresh()
        elif key in (ord('\n'), ord(' ')):
            return self.items[self.selected_item][1]
        return None


class RightPanel:
    DEFAULT_X = 26

    def __init__(self, stdscr):
        self._stdscr = stdscr

        self.data = {
            0: ["Все обсуждения: тема 1", "тема 2", "тема 3"],
            1: ["Мои темы: пост 1", "пост 2"],
            2: ["Прочитанные темы: запись 1", "запись 2"],
            3: ["Закладки: сохранено 1", "сохранено 2"],
            4: ["Отложенные темы: отложено 1"],
            5: ["Халява: бесплатно 1", "бесплатно 2"],
            6: ["Торговля: товар 1", "товар 2"],
            7: ["Работа и услуги: вакансия 1"],
            8: ["Арбитраж: спор 1", "спор 2"],
        }
        self.selected_data = None

        self.subscr = stdscr.subwin(0, 0, 0, self.DEFAULT_X)

    def render(self):
        self.subscr.resize(root_scr_y, max(1, root_scr_x - self.DEFAULT_X))
        self.subscr.box()

        if self.selected_data is not None and self.selected_data in self.data:
            for i, item in enumerate(self.data[self.selected_data]):
                try:
                    self._stdscr.addstr(i + 1, self.DEFAULT_X + 3, str(item))
                except curses.error:
                    pass

    def render_and_refresh(self):
        self.render()
        self.subscr.refresh()

    def resize(self):
        self.subscr.erase()
        self.render_and_refresh()

    def update_data(self, item_id):
        self.selected_data = item_id
        self.subscr.erase()
        self.render_and_refresh()


class V2:
    __slots__ = ("y", "x")

    def __init__(self, y=0, x=0):
        if isinstance(y, tuple):
            self.y = y[0]
            self.x = y[1]
        else:
            self.y = y
            self.x = x

    def __repr__(self):
        return f"y={self.y} x={self.x}"


class BasePanel(ABC):
    DEFAULT_Y = 0
    DEFAULT_X = 0
    DEFAULT_ROWS = 0
    DEFAULT_COLS = 0

    def __init__(self, parent):
        self.parent = parent

        self.subwin = parent._stdscr.subwin(
            self.DEFAULT_ROWS,
            self.DEFAULT_COLS,
            self.DEFAULT_Y,
            self.DEFAULT_X
        )
        self.subwin.clear()

    @abstractmethod
    def render(self): ...

    def render_and_refresh(self):
        self.render()
        self.subwin.refresh()

    def clear_and_render(self):
        self.subwin.erase()
        self.render()

    def resize(self):
        self.subwin.erase()
        self.render_and_refresh()

    def addstr(self, y, x, text, *attrs):
        try:
            self.subwin.addstr(y, x, text, *attrs)
        except:
            pass


class CategoryPanelA(BasePanel):
    DEFAULT_COLS = 30
    
    def __init__(self, parent):
        super().__init__(parent)

        self.items = [
            ("Профиль", None),
            ("Все обсуждения", 0),
            ("Мои темы", 1),
            ("Прочитанные темы", 2),
            ("Закладки", 3),
            ("Отложенные темы", 4),
            ("Основная категория", None),
            ("Халява", 5),
            ("Торговля", 6),
            ("Работа и услуги", 7),
            ("Арбитраж", 8),
            ("Тематическая категория", None),
            ("Тематические вопросы", 9),
            ("Спроси у ChatGPT", 10),
            ("Статьи", 11),
            ("Софт", 11),
            ("Игровая категория", None),
            ("PUBG", 12),
            ("Counter-Strike 2", 12),
            ("Dota 2", 12),
            ("Overwatch 2", 12),
            ("Fortnite", 12),
            ("Valorant", 12),
            ("GTA", 12),
            ("World of Tanks", 12),
            ("miHoYo", 12),
            ("Deadlock", 12),
            ("Остальные игры", 12),
            ("Общая категория", None),
            ("Оффтопик", 2),
            ("Компьютеры", 2),
            ("Телефоны", 2),
            ("Веб-разработка", 2),
            ("Программирование", 2),
            ("Графика", 2),
            ("Жизнь форума", 2),
            ("Тестовый раздел", 2),
        ]
        self.selected_item = 1
        self.scroll_offset = 0

    def render(self):
        if self.DEFAULT_COLS > self.parent._sx:
            self.subscr_cols = self.parent._sx
        elif self.DEFAULT_COLS < self.parent._sx:
            self.DEFAULT_COLS = min(self.DEFAULT_COLS, self.parent._sx)

        try:
            self.subwin.resize(self.parent._sy, self.DEFAULT_COLS)
        except:
            pass
        self.subwin.box()

        max_lines = self.parent._sy - 2
        y, x = 1, 3

        if self.selected_item == 1 and self.scroll_offset == 1:
            self.scroll_offset = 0
            self.clear_and_render()
        elif self.selected_item < self.scroll_offset:
            self.scroll_offset = self.selected_item
            self.clear_and_render()
        elif self.selected_item >= self.scroll_offset + max_lines:
            self.scroll_offset = self.selected_item - max_lines + 2
            self.clear_and_render()

        for i in range(self.scroll_offset, min(self.scroll_offset + max_lines, len(self.items))):
            item_name, item_id = self.items[i]
            color = 1 if i == self.selected_item else 0

            if item_id is None:
                if i != 0:
                    y += 1

                if y >= max_lines + 1:
                    break

                self.addstr(y, x, f"[{item_name}]", curses.color_pair(color))
                y += 1
            else:
                self.addstr(y, x, f"- {item_name.ljust(18)}", curses.color_pair(color))
                y += 1

            if y >= max_lines + 1:
                break

    def event(self, key):
        if key == ord('k'):
            new_pos = self.selected_item - 1
            while new_pos > 0:
                if self.items[new_pos][1] is not None:
                    self.selected_item = new_pos
                    break
                new_pos -= 1
            self.render_and_refresh()
        elif key == ord('j'):
            new_pos = self.selected_item + 1
            while new_pos < len(self.items):
                if self.items[new_pos][1] is not None:
                    self.selected_item = new_pos
                    break
                new_pos += 1
            self.render_and_refresh()


class CategoryPanel(BasePanel):
    DEFAULT_COLS = 30
    
    def __init__(self, parent):
        super().__init__(parent)
        self.categories = [
            ("Профиль", None),
            ("Все обсуждения", 0),
            ("Мои темы", 1),
            ("Прочитанные темы", 2),
            ("Закладки", 3),
            ("Отложенные темы", 4),
            ("Основная категория", None),
            ("Халява", 5),
            ("Торговля", 6),
            ("Работа и услуги", 7),
            ("Арбитраж", 8),
            ("Тематическая категория", None),
            ("Тематические вопросы", 9),
            ("Спроси у ChatGPT", 10),
            ("Статьи", 11),
            ("Софт", 11),
            ("Игровая категория", None),
            ("PUBG", 12),
            ("Counter-Strike 2", 12),
            ("Dota 2", 12),
            ("Overwatch 2", 12),
            ("Fortnite", 12),
            ("Valorant", 12),
            ("GTA", 12),
            ("World of Tanks", 12),
            ("miHoYo", 12),
            ("Deadlock", 12),
            ("Остальные игры", 12),
            ("Общая категория", None),
            ("Оффтопик", 2),
            ("Компьютеры", 2),
            ("Телефоны", 2),
            ("Веб-разработка", 2),
            ("Программирование", 2),
            ("Графика", 2),
            ("Жизнь форума", 2),
            ("Тестовый раздел", 2),
        ]
        self.selected_category = 1
        self.scroll_offset = 0
        self.cursor_pos = 0
        
    def render(self):
        if self.DEFAULT_COLS > self.parent._sx:
            self.DEFAULT_COLS = self.parent._sx
        elif self.DEFAULT_COLS < self.parent._sx:
            self.DEFAULT_COLS = min(self.DEFAULT_COLS, self.parent._sx)

        try:
            self.subwin.resize(self.parent._sy, self.DEFAULT_COLS)
        except:
            pass

        center_y = self.parent._sy // 2
        visible_lines = self.parent._sy - 2
        half_visible = visible_lines // 2

        if self.selected_category < self.scroll_offset + half_visible:
            self.scroll_offset = max(0, self.selected_category - half_visible)
            self.subwin.erase()
        elif self.selected_category > self.scroll_offset + half_visible:
            self.scroll_offset = min(max(0, len(self.categories) - visible_lines), self.selected_category - half_visible)
            self.subwin.erase()

        self.subwin.box()

        y_start = 1
        x = 3

        for i in range(self.scroll_offset, min(self.scroll_offset + visible_lines, len(self.categories))):
            rel_y = i - self.scroll_offset
            y = y_start + rel_y
            
            category_name, category_id = self.categories[i]
            color = 1 if i == self.selected_category else 0
            
            if category_id is None:
                self.addstr(y, x, f"[{category_name}]", curses.color_pair(color))
                y += 1
            else:
                self.addstr(y, x, f"- {category_name.ljust(self.DEFAULT_COLS - 8)}", curses.color_pair(color))

    def event(self, key):
        old_selection = self.selected_category
        
        if key == ord('k'):
            new_pos = self.selected_category - 1
            while new_pos >= 0:
                if self.categories[new_pos][1] is not None:
                    self.selected_category = new_pos
                    break
                new_pos -= 1
        elif key == ord('j'):
            new_pos = self.selected_category + 1
            while new_pos < len(self.categories):
                if self.categories[new_pos][1] is not None:
                    self.selected_category = new_pos
                    break
                new_pos += 1
        elif key in (ord('\n'), ord(' ')):
            return self.categories[self.selected_category][1]
        
        if old_selection != self.selected_category:
            return "update"
        
        return None

class Application:
    def __init__(self):
        self.init_screen()
        self.init_colors()
        self.init_panels()

        self._sy = self._sx = 0
        self._old_sy = self._old_sx = 0

        self.key = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self._stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def init_screen(self):
        self._stdscr = curses.initscr()
        curses.noecho()

    def init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def init_panels(self):
        self.panels = [CategoryPanel(self)]

    def update(self):
        self._sy, self._sx = self._stdscr.getmaxyx()

        for panel in self.panels:
            if self.is_resized:
                self._old_sy, self._old_sx = self._sy, self._sx
                panel.resize()

            panel.render()

            result = panel.event(self.key)
            if result == "update":
                panel.render_and_refresh()

        self.key = self._stdscr.getch()

    def should_close(self):
        return self.key == ord('q')

    @property
    def size(self):
        return self._sy, self._sx

    @property
    def is_resized(self):
        return self._old_sy != self._sy or self._old_sx != self._sx



if __name__ == "__main__":
    app = Application()
    try:
        while not app.should_close():
            app.update()
    finally:
        app.close()
