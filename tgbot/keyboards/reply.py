from dataclasses import dataclass

from tgbot.config import ListOfButtons


@dataclass
class FQ:
    exit: str = 'Можно ли выйти с выпускного и зайти повторно?'
    items: str = 'Что взять с собой?'
    water: str = 'Будет ли на площадке вода?'
    timing: str = 'До скольки будут активности?'
    fireworks: str = 'Во сколько и где будет проходить салют?'
    main_menu: str = 'Главное меню'


@dataclass
class Events:
    main_scene: str = "⭐️Главная сцена"
    quay_scene: str = "⛵️Электросцена"
    water_show: str = "🎭Шоу на воде"
    disco_scene: str = "🕺Диско-сцена"
    quiet_disco: str = "🎧Тихая дискотека"
    game_zone: str = "🎮Киберспорт"
    quiz_please: str = "🧠Интеллектуальная игра"
    comic_show: str = "😁Комик-шоу"
    extreme: str = "🛹Экстремальный спорт"
    young_people: str = "👫Молодежь Москвы"
    main_menu: str = "🔙Главное меню"


@dataclass
class ROLE:
    grad: str = 'Выпускник'
    teacher: str = 'Учитель'
    parents: str = 'Родитель'


MAIN_MENU = ListOfButtons(
    text=[
        "Программа", "Карта", "Отзывы", "Сообщение в чат\nили на экран",
        "Фотоальбом", "Стикерпак", "Онлайн-чат", "Справка"
    ],
    align=[2, 2, 2, 2]
).reply_keyboard

EVENTS = ListOfButtons(
    text=[Events.main_scene,
          Events.quay_scene,
          Events.water_show,
          Events.disco_scene,
          Events.quiet_disco,
          Events.game_zone,
          Events.quiz_please,
          Events.comic_show,
          Events.extreme,
          Events.young_people,
          Events.main_menu],
    align=[2, 2, 2, 2, 2, 1]
).reply_keyboard

REVIEW_ANSWER = ListOfButtons(
    text=[ROLE.grad,
          ROLE.teacher,
          ROLE.parents],
    align=[1, 1, 1]
).reply_keyboard

FAQ = ListOfButtons(
    text=[FQ.exit,
          FQ.items,
          FQ.water,
          FQ.timing,
          FQ.fireworks,
          FQ.main_menu],
    align=[1, 2, 1, 2]
).reply_keyboard
