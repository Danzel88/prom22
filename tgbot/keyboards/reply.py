from tgbot.config import ListOfButtons

MAIN_MENU = ListOfButtons(
    text=[
        "Программа", "Карта", "Отзывы", "Сообщение на экран",
        "Фотоальбом", "Стикерпак", "Справка"
    ],
    align=[2, 2, 2, 1]
).reply_keyboard


EVENTS = ListOfButtons(
    text=[
        "⭐️Главная сцена",
        "⛵️Сцена на набережной",
        "🎭Театр на воде",
        "🕺Ретродискотека",
        "🎧Тихая дискотека. Пой, Танцуй!",
        "🎮Зона компьютерных игр",
        "🧠Квиз!Плиз!",
        "😁Комик-шоу",
        "🛹Экстрим-площадка",
        "🔙Гланое меню"

    ],
    align=[1,1,1,1,1,1,1,1,1,1]
).reply_keyboard


REVIEW_ANSWER = ListOfButtons(
    text=[
        "Выпускник",
        "Учитель",
        "Родитель"
    ],
    align=[1, 1, 1]
).reply_keyboard
