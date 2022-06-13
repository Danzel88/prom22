import re
from .bw import l


async def censor(text):
    word = re.findall(r'\w+', text)
    tmp_array = []
    for bw in l:
        tmp_array.append(bw['fields']['word'])
    return set(word).isdisjoint(set(tmp_array))
