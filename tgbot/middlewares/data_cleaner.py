import logging
from asyncio import sleep


async def cleaner(data: dict, context: str) -> list:
    match context:
        case "Chat:wait_text":
            try:
                del(data['username'], data['role'], data['pers_info'], data['review'])
            except KeyError as er:
                logging.info("Clean data for chat message")
            finally:
                return list(data.values())
        case "Review:wait_review":
            try:
                del (data['username'], data['name'], data['school'], data['text'])
            except KeyError as er:
                logging.info("Clean data for review")
            finally:
                return list(data.values())


async def format_msg_to_chat(msg: list):
    del(msg[0], msg[-1])
    res = f'<b>{msg[0]}</b>, <b>школа {msg[1]}</b>\n\n{msg[-1]}'
    await sleep(1)
    return res


