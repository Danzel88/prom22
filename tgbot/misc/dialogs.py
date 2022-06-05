from dataclasses import dataclass


@dataclass(frozen=True)
class Messages:
    grete_msg: str = "Привет!"
    retry_start: str = "Ты уже стартовал. Будешь получать новости. Юзай меню."
    start_review: str = "Напиши как тебе мероприятие"
    finish_review: str = "Спасибо, отзыв поличили, гуляй дальше"
    start_common_chat: str = "Отправь сообщение, оно будет показано на главном экране. " \
                             "Не матерись, политические взгляды дерди при себе, " \
                             "и вообще будь разумным по жизни"