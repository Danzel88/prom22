from dataclasses import dataclass


@dataclass(frozen=True)
class Messages:
    main_menu_description: str = "Ты снова в главном меню. Выбери интересующий пункт 👇"
    grete_msg: str = "Привет и добро пожаловать на Московский выпускной 2022! " \
                     "Давай сделаем всё, чтобы эта ночь стала запоминающейся, " \
                     "веселой, душевной и осталась в памяти навсегда ✨ Погнали?\n\n" \
                     "Открывай меню и выбирай, что тебя интересует."

    grete_msg2: str = "Открывай меню и выбирай, что тебя интересует."
    main_menu: str = "Главное меню"
    event_program: str = "В парке ты найдешь 9 основных локаций, и у каждой есть своя программа. " \
                         "Выбери локацию и посмотри, что тебя там ждет."
    map: str = "Это карта нашего праздника. " \
               "С ней ты точно не заблудишься и успеешь посетить все локации.\n\n" \
               "Узнай, где находятся фотозоны, где можно поиграть в квиз " \
               "или компьютерные игры, а где потанцевать или " \
               "посмотреть выступления стендап-комиков 🗺"
    start_review: str = "Хочешь поделиться впечатлениями от выпускного? " \
                        "Тогда оставляй свой отзыв. " \
                        "Но помни, что написать его можно только один раз."
    user_role: str = "Начнем? В качестве кого ты был(а) на выпускном?"
    pers_info_for_grad: str = "И еще для формальности напиши одним сообщением," \
                              " как тебя зовут и из какой ты школы?"
    pers_info_for_parents: str = "Мое почтение! В таком случае предлагаю " \
                                  "перейти на «вы».\n\nКак вас зовут и из какой" \
                                  " школы ваш ребенок? Напишите одним сообщением."

    pers_info_for_teacher: str = "Мое почтение! В таком случае предлагаю " \
                                  "перейти на «вы».\n\nКак вас зовут и из какой школы вы школы? " \
                                 "Напишите одним сообщением."
    pers_info: str = "И еще для формальности напиши, как тебя зовут и из какой ты школы?"
    review_name: str = "И еще для формальности напиши, как тебя зовут"
    review_school: str = "И из какой ты школы"
    comment_invite: str = "Ну а теперь жду рассказ о впечатлениях: что больше всего понравилось?" \
                          " Или, наоборот, что можно улучшить?"
    finish_review: str = "Спасибо за отзыв!\nОбязательно передам всё своим " \
                         "коллегам ❤️"

    msg_to_all: str = "💥Как насчет того, чтобы войти в историю Московского выпускного 2022?\n\n" \
                      "Тогда отправляй сообщение — оно появится в онлайн-чате и на экранах главной" \
                      " сцены. Передавай приветы, признавайся в любви и делись секретами — твой " \
                      "месседж увидят все гости вечера!\n\n❗️А чтобы послание гарантированно прошло" \
                      " модерацию, есть главное правило — никаких оскорблений и матов, " \
                      "ссылок на сторонние ресурсы и спама.\n\nСообщения публикуются в " \
                      "порядке очереди. Начнем?"

    name_for_main_chat: str = "Как тебя зовут?"
    school_for_main_chat: str = "Напиши номер школы."
    text_for_main_chat: str = "Жду твое сообщение! " \
                              "Самые интересные послания попадают еще и " \
                              "на экраны главной сцены🔥"
    msg_for_main_chat_done: str = "Твои слова — разрыв сердечка!\nА теперь " \
                                  "подожди немного. Скоро сообщение появится" \
                                  " в чате. А может, и на экране 👀"

    photo_link: str = "📸 Улыбнись, тебя снимают!\nДаже когда ты этого не " \
                      "замечаешь, поэтому улыбайся всегда 🙂\n\nА самые яркие " \
                      "моменты вечера и фотки себя и друзей ищи по ссылке, " \
                      "которая постоянно пополняется 👉"

    tmp_photo_link: str = "📸Улыбайся чаще!\n\nНаши фотографы будут ловить самые яркие моменты " \
                          "выпускного, поэтому не стесняйся им позировать.\n\nСкоро я размещу " \
                          "здесь ссылку на фотографии. Сможешь найти себя и друзей 💕"

    sticker_pack_first: str = "Зацени, какие крутые стикеры у меня есть. " \
                              "Огонь, правда? 🔥\n\nСкорее добавляй себе и " \
                              "отправляй друзьям."
    sticker_pack_second: str = "Хочешь дополнить стикерпак чем-то своим?\n\n" \
                               "1️⃣Придумай классную короткую фразу.\n" \
                               "2️⃣Напиши ее в ответ с пометкой «Мой стикер» в начале сообщения.\n" \
                               "3️⃣Самые крутые фразы появятся в стикерпаке" \
                               " Московского выпускного 2022."
    faq_description: str = "Ответы на самые важные вопросы👇"

    retry_start: str = "О, я тебя помню!\n\nЗаходи в меню, тут собрано всё, " \
                       "что я умею. Например, могу поделиться расписанием " \
                       "площадок, показать фотографии или ответить на важные " \
                       "вопросы 🤟"
    online_chat: str = "💬Онлайн-чат для твоих сообщений с приветами, поздравлениями, " \
                        "признаниями и пожеланиями.\n\n1️⃣Присылай через команду /msg_to_all " \
                        "или кнопку меню «Сообщение в чат или на экран»\n2️⃣Заходи смотреть\n" \
                        "3️⃣Общайся с другими выпускниками\n\nВсе сообщения проходят модерацию и " \
                        "публикуются в порядке очереди."
    retry_review: str = "Твой отзыв уже есть"
    not_in_answers_list: str = "Выбери один из предложенных вариантов 🤔"
    censor_stop: str = "Я всё вижу и не пропускаю:\n\n🚫 мат и оскорбления;\n" \
                       "🚫 призывы к насилию;\n🚫 ссылки на сторонние ресурсы;\n" \
                       "🚫 спам.\n\nПопробуешь еще раз?"
    its_commands: str = "Из команд поддерживается только /menu для выхода в Главное меню"
    only_text: str = "Я публикую только текст и эмоджи. " \
                     "Стикеры, фотографии или картинки оставляю " \
                     "себе на память 😉"

@dataclass(frozen=True)
class FaqAnswers:
    exit_chance = 'На выпускном есть только 1 сеанс входа и 1 сеанс выхода с ' \
                  'мероприятия. То есть, если ты решишь выйти с площадки, ' \
                  'то уже не сможешь зайти обратно.'
    personal_items = 'Рекомендуем взять с собой телефон, сменную обувь, косметику ' \
                     '(если нужно поправить макияж), верхнюю одежду и небольшую ' \
                     'сумму денег (чтобы подкрепиться на фудкорте). А вот ' \
                     'проносить любые жидкости, баллончики, колюще-режущие предметы' \
                     ' и оружие запрещено. На входе это тщательно проверяется.'
    water: str = 'Да, на территории парка будут стоять точки с бесплатной водой. ' \
                 'Все локации можно посмотреть на карте.'
    timing: str ='Анимационные площадки работают до 04:00. С 04:00 до 06:00' \
                 ' пройдет дискотека. '
    fireworks: str = 'Салют начнется ровно в 00:00. Запуск будет прямо с ' \
                     'Москвы-реки, поэтому лучший обзор откроется с ' \
                     'Пушкинской набережной.'


@dataclass(frozen=True)
class SenderMessages:
    message_for_sender: str = "Это функция рассылки. Сообщения будут отправлены всем пользователям бота." \
                              " Пришли сообщение, которое нужно разослать.\n" \
                              "<b>НЕ ЗАБУДЬ ПРОВЕРИТЬ ТЕСТОВОЙ РАССЫЛКОЙ!!!</b>\n/test_sender"
    message_for_test_sender: str = "Тестовая отправка сообщения перед рассылкой всем пользователям!\n" \
                                   "<b>НЕ ЗАБУДЬ ОТПРАВИТЬ ВСЕМ</b>"


@dataclass(frozen=True)
class NoPicProgram:
    young_people: str = "🔹Время работы: с 20:00 до 04:00.\n\n" \
                        "Музыкальная игра Just Dance\n\n" \
                        "▪️Мастер-классы\n" \
                        "▪️Свободная зона Just Dance\n" \
                        "▪️Флешмоб «Танцуют все»\n" \
                        "▪️Презентация проектов КОСиМП"

    quiet_disco: str = "🔹Время работы: с 20:00 до 04:00.\n" \
                       "🔹Продолжительность сеанса: 15 минут.\n\n" \
                       "Арт-объект, где каждый получает индивидуальную " \
                       "пару наушников и оказывается на самой захватывающей " \
                       "и тихой дискотеке в мире.\n\nПовторяй простые " \
                       "движения, слушай ведущего и расслабляйся. " \
                       "Сможешь узнать себя и окружающих с неожиданной " \
                       "стороны, по-новому взглянуть на пространство и" \
                       " надолго запомнить выпускную ночь✨"
    game_zone: str = "🔹Время работы: с 20:00 до 04:00.\n\n" \
                     "Локация, где ты можешь показать свое мастерства" \
                     " в DOTA 2, Valorant, CS:GO, World of Tanks," \
                     " FIFA 21. Окунуться в виртуальную реальность." \
                     " Посетить фотозону-косплей с популярными персонажами" \
                     " игрового мира."
    quiz_please: str = "🔹Время работы: с 20:00 до 04:00.\n" \
                       "🔹Продолжительность сеанса: 25 минут.\n\n" \
                       "Развлекательная интеллектуальная битва, " \
                       "вопросы для которой созданы специально для" \
                       " Московского Выпускного 2022."
    extreme_old: str = "Время работы: с 20:00 до 04:00.\n\n" \
                    "<b>️Фристайл байк-шоу</b>\n\n" \
                    "\t • Выступления топовых райдеров России.\n" \
                    "\t • Зрелищные экстремальные трюки на BMX, MTB, " \
                    "кикскутере.\n\n" \
                    "🏀Стритбол\n\n" \
                    "\t • Соревнования среди команд выпускников.\n" \
                    "\t • Мастер-классы от профессиональных спортсменов.\n\n" \
                    "⚽️<b>Панна-футбол</b>\n\n" \
                    "\t • Показательные выступления и мастер-классы от профессиональных спортсменов.\n" \
                    "\t • Соревнования среди выпускников.\n\n" \
                    "🎧<b>Dj-сеты</b>"
    extreme: str = "Время работы: с 20:00 до 04:00.\n\n" \
                "🚴‍♂️<b>Фристайл байк-шоу</b>\n\n▪️Выступления топовых райдеров России.\n" \
               "▪️Зрелищные экстремальные трюки на BMX, MTB, кикскутере.\n\n" \
               "🏀️<b>Стритбол</b>\n\n" \
               "▪️Соревнования среди команд выпускников.\n" \
               "▪️Мастер-классы от профессиональных спортсменов.\n\n" \
               "⚽️<b>Панна-футбол</b>\n\n" \
               "▪️Показательные выступления и мастер-классы от профессиональных спортсменов.\n" \
               "▪️Соревнования среди выпускников.\n\n" \
               "🎧<b>Dj-сеты</b>\n\n"
