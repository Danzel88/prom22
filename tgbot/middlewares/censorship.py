import re
from tgbot.middlewares.bw_list import stop_words


async def censor(text):
    word = re.findall(r'\w+', text)

    return set(word).isdisjoint(set(stop_words))
