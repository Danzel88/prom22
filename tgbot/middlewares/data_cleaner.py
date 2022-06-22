import logging

from aiogram.dispatcher.filters.state import State


async def cleaner(data: dict, context: str) -> list:
    print(context)
    match context:
        case "Chat:wait_text":
            try:
                del(data['username'], data['role'], data['pers_info'], data['review'])
            except KeyError as er:
                print(er)
            finally:
                return list(data.values())
        case "Review:wait_review":
            try:
                del (data['username'], data['name'], data['school'], data['text'])
            except KeyError as er:
                print(er)
            finally:
                return list(data.values())

