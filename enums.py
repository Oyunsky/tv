__all__ = [
    "ThreadCategory",
    "TC",
    "ThreadCategories",
]

from enum import Enum, auto


class ThreadCategory(Enum):
    ALL_DISCUSSION     = auto()
    MY_THREADS         = auto()
    VIEWED_THREADS     = auto()
    BOOKMARKS          = auto()
    SCHEDULED_THREADS  = auto()

    FREEBIES           = auto()
    TRADE              = auto()
    WORK_AND_SERVICES  = auto()
    ARBITRATION        = auto()

    THEMATIC_QUESTIONS = auto()
    ASK_CHATGPT        = auto()
    ARTICLES           = auto()
    SOFTWARE           = auto()

    PUBG               = auto()
    COUNTER_STRIKE_2   = auto()
    DOTA_2             = auto()
    OVERWATCH_2        = auto()
    FORTNITE           = auto()
    VALORANT           = auto()
    GTA                = auto()
    WORLD_OF_TANKS     = auto()
    MIHOYO             = auto()
    DEADLOCK           = auto()
    OTHER_GAMES        = auto()

    OFFTOPIC           = auto()
    COMPUTERS          = auto()
    PHONES             = auto()
    WEB_DEVELOPMENT    = auto()
    PROGRAMMING        = auto()
    GRAPHICS           = auto()
    FORUM_LIFE         = auto()
    TEST_SECTION       = auto()

    @property
    def title(self):
        return {
            ThreadCategory.ALL_DISCUSSION:     "Все обсуждения",
            ThreadCategory.MY_THREADS:         "Мои темы",
            ThreadCategory.VIEWED_THREADS:     "Прочитанные темы",
            ThreadCategory.BOOKMARKS:          "Закладки",
            ThreadCategory.SCHEDULED_THREADS:  "Отложенные темы",

            ThreadCategory.FREEBIES:           "Халява",
            ThreadCategory.TRADE:              "Торговля",
            ThreadCategory.WORK_AND_SERVICES:  "Работа и услуги",
            ThreadCategory.ARBITRATION:        "Арбитраж",

            ThreadCategory.THEMATIC_QUESTIONS: "Тематические вопросы",
            ThreadCategory.ASK_CHATGPT:        "Спроси у ChatGPT",
            ThreadCategory.ARTICLES:           "Статьи",
            ThreadCategory.SOFTWARE:           "Софт",

            ThreadCategory.PUBG:               "PUBG",
            ThreadCategory.COUNTER_STRIKE_2:   "Counter-Strike 2",
            ThreadCategory.DOTA_2:             "Dota 2",
            ThreadCategory.OVERWATCH_2:        "Overwatch 2",
            ThreadCategory.FORTNITE:           "Fortnite",
            ThreadCategory.VALORANT:           "Valorant",
            ThreadCategory.GTA:                "GTA",
            ThreadCategory.WORLD_OF_TANKS:     "World of Tanks",
            ThreadCategory.MIHOYO:             "miHoYo",
            ThreadCategory.DEADLOCK:           "Deadlock",
            ThreadCategory.OTHER_GAMES:        "Остальные игры",

            ThreadCategory.OFFTOPIC:           "Оффтопик",
            ThreadCategory.COMPUTERS:          "Компьютеры",
            ThreadCategory.PHONES:             "Телефоны",
            ThreadCategory.WEB_DEVELOPMENT:    "Веб-разработка",
            ThreadCategory.PROGRAMMING:        "Программирование",
            ThreadCategory.GRAPHICS:           "Графика",
            ThreadCategory.FORUM_LIFE:         "Жизнь форума",
            ThreadCategory.TEST_SECTION:       "Тестовый раздел",
        }[self]


TC = ThreadCategory

ThreadCategories = [
    ("Меню", None),
    ("Все обсуждения", TC.ALL_DISCUSSION),
    ("Мои темы", TC.MY_THREADS),
    ("Прочитанные темы", TC.VIEWED_THREADS),
    ("Закладки", TC.BOOKMARKS),
    ("Отложенные темы", TC.SCHEDULED_THREADS),

    ("Основная категория", None),
    ("Халява", TC.FREEBIES),
    ("Торговля", TC.TRADE),
    ("Работа и услуги", TC.WORK_AND_SERVICES),
    ("Арбитраж", TC.ARBITRATION),

    ("Тематическая категория", None),
    ("Тематические вопросы", TC.THEMATIC_QUESTIONS),
    ("Спроси у ChatGPT", TC.ASK_CHATGPT),
    ("Статьи", TC.ARTICLES),
    ("Софт", TC.SOFTWARE),

    ("Игровая категория", None),
    ("PUBG", TC.PUBG),
    ("Counter-Strike 2", TC.COUNTER_STRIKE_2),
    ("Dota 2", TC.DOTA_2),
    ("Overwatch 2", TC.OVERWATCH_2),
    ("Fortnite", TC.FORTNITE),
    ("Valorant", TC.VALORANT),
    ("GTA", TC.GTA),
    ("World of Tanks", TC.WORLD_OF_TANKS),
    ("miHoYo", TC.MIHOYO),
    ("Deadlock", TC.DEADLOCK),
    ("Остальные игры", TC.OTHER_GAMES),

    ("Общая категория", None),
    ("Оффтопик", TC.OFFTOPIC),
    ("Компьютеры", TC.COMPUTERS),
    ("Телефоны", TC.PHONES),
    ("Веб-разработка", TC.WEB_DEVELOPMENT),
    ("Программирование", TC.PROGRAMMING),
    ("Графика", TC.GRAPHICS),
    ("Жизнь форума", TC.FORUM_LIFE),
    ("Тестовый раздел", TC.TEST_SECTION)
]
