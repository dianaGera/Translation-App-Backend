import asyncio
import time
from contextlib import contextmanager
import requests
from bs4 import BeautifulSoup
from django.db import connection
from django.db import close_old_connections

vocab = 'https://wooordhunt.ru/dic/content/en_ru'


@contextmanager
def processor():
    start = time.time()
    print(f'Processes start at ---> {time.strftime("%X")}')
    yield
    finish = time.time()
    print(f'Processes end at ---> {time.strftime("%X")}',
          f'Total time is equal {(finish - start)/60} min or {finish - start} sec for in word', sep='\n')


def pars_word(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    def get_en_word():
        en_word_parse = soup.find('h1')
        en_word = []
        if en_word_parse:
            for i in en_word_parse:
                en_word.append(i.get_text().strip())
                break
            return en_word

    async def get_translate():
        translate_parse = soup.find('div', class_='t_inline_en')
        translate, c = [], []
        if translate_parse:
            for i in translate_parse:
                c = i.get_text().split(',')
                for j in c:
                    translate.append(j.strip())
            return translate

    async def get_part_of_speech():
        part_of_speech_parse = soup.find_all('h4', class_='pos_item')
        part_of_speech = []
        for i in part_of_speech_parse:
            if i.get_text()[-1] == ' ' or i.get_text()[-1] == '↓':
                part_of_speech.append(i.get_text()[0:-2])
            else:
                part_of_speech.append(i.get_text())
        return part_of_speech

    async def get_hidden_collacation():
        block = soup.find_all('div', class_='ex')
        c, hidden_collacation = [], {}
        for i in block:
            c += i.get_text().split('\u2002')
        for i in range(1, len(c)):
            if c[i] == '—':
                hidden_collacation[c[i-1]] = c[i+1]
        return hidden_collacation

    async def get_coll_and_phrases():
        block = soup.find_all('div', class_='block')
        lst = []
        for i in block:
            lst.append(i.get_text().split('\xa0'))
        r, c, coll, phrases = [], [], {}, {}
        print(lst)
        for i in range(1, len(lst)):
            if i == 1:
                for j in range(len(lst[i])-1):
                    r.append(lst[i][j].strip().split('\u2002—\u2002'))
            elif i > 1:
                for j in lst[i]:
                    for p in j.split('\u2002'):
                        c.append(p.strip())
                        if len(c) == 2:
                            r.append(c)
                            c = []
        for i in range(len(r)):
            if len(r[i]) > 1:
                if r[i][0].islower():
                    if r[i][0][0] <= 'А' and r[i][0][1] != '—':
                        if len(r[i][1]) > 1:
                            coll[r[i][0]] = r[i][1]
                if len(r[i][0]) > 1 and r[i][0][0].isupper():
                    if len(r[i]) > 1:
                        phrases[r[i][0]] = r[i][1]
        return coll, phrases

    async def get_audio():
        audio_pars_src = soup.find_all('source')
        audio = []
        for a in audio_pars_src:
            audio.append('https://wooordhunt.ru' + a['src'])
        return audio

    async def get_cognate_word():
        block = soup.find_all('div', class_='similar_words')
        c, lst, cognate_word, en = '', [], {}, []
        for i in block:
            lst += i.get_text().split("\u2002—\u2002")
        if len(lst) > 0:
            c = lst[0].strip()
        for i in range(1, len(lst)):
            if c != '':
                cognate_word[c] = ' '.join(map(str, list(filter(lambda x: x if x >= 'А' else None, lst[i].split(' ')))))
                en = list(filter(lambda x: x if x <= 'А' else None, lst[i].split(' ')[-2::]))
                c = ' '.join(map(str, en))
        return cognate_word

    en_word_list = get_en_word()
    translate_list = asyncio.run(get_translate())
    part_of_speech_list = asyncio.run(get_part_of_speech())
    hidden_collacation_dict = asyncio.run(get_hidden_collacation())
    coll2_dict, phrases_dict = asyncio.run(get_coll_and_phrases())
    audio_list = asyncio.run(get_audio())
    coll_dict = {**hidden_collacation_dict, **coll2_dict}
    cognate_word_dict = asyncio.run(get_cognate_word())
    print('en_word_list ---------', en_word_list)
    print('translate_list -------', translate_list)
    print('part_of_speech_list --', part_of_speech_list)
    print('coll_dict ------------', coll_dict)
    print('cognate_word_dict ----', cognate_word_dict)
    print('phrases --------------', phrases_dict)
    print('audio_list -----------', audio_list)


    if en_word_list:
        for word in en_word_list:
            word = EnWord.objects.create(
                word=word,
                audio_us=str(audio_list[0] if len(audio_list) > 0 else 'None'),
                audio_uk=str(audio_list[1] if len(audio_list) > 1 else 'None'))
            obj = []
            if translate_list:
                for tr in translate_list:
                    try:
                        translate_word = RuWord.objects.get(word=tr)
                        obj.append(translate_word)
                    except:
                        translate_word = RuWord(word=tr)
                        translate_word.save()
                        obj.append(translate_word)
                word.translate.add(*obj)
                obj = []
            for prt in part_of_speech_list:
                try:
                    part_of_speech = PartOfSpeech.objects.get(part_of_speech=prt)
                    obj.append(part_of_speech)
                except:
                    part_of_speech = PartOfSpeech(part_of_speech=prt)
                    part_of_speech.save()
                    obj.append(part_of_speech)
            word.part_of_speech.add(*obj)
            obj = []
            for ph in phrases_dict:
                try:
                    phrase = Phrase.objects.get(en_phrase=ph)
                    obj.append(phrase)
                except:
                    phrase = Phrase(en_phrase=ph,
                                    ru_phrase=phrases_dict[ph])
                    phrase.save()
                    obj.append(phrase)
            word.phrase.add(*obj)
            obj = []
            for cl in coll_dict:
                try:
                    coll = Collocation.objects.get(en_collocation=cl)
                    obj.append(coll)
                except:
                    coll = Collocation(en_collocation=cl,
                                       ru_collocation=coll_dict[cl])
                    coll.save()
                    obj.append(coll)
            word.collocation.add(*obj)
            obj = []
            for cog in cognate_word_dict:
                try:
                    cognate = CognateWord.objects.get(en_cognate_word=cog)
                    obj.append(cognate)
                except:
                    cognate = CognateWord(en_cognate_word=cog,
                                          ru_cognate_word=cognate_word_dict[cog])
                    cognate.save()
                    obj.append(cognate)
            word.cognate_word.add(*obj)
            obj = []
            connection.close()


def get_url(url_list):
    with processor():
        for url in url_list:
            close_old_connections()
            yield pars_word(url)


def all_links(page):
    response = requests.get(page)
    soup = BeautifulSoup(response.text, 'lxml')
    all_links = soup.find_all('a')
    links, x = [], False
    for i in all_links:
        if len(i.get_text()) == 2:
            links.append('https://wooordhunt.ru' + i['href'])
    links = links[links.index('https://wooordhunt.ru/dic/list/en_ru/sg')::]
    return find_word_link(links)


def find_word_link(links):
    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')
        all_p = soup.find_all('p')
        words_links, x = [], False
        for p in all_p:
            words_links.append('https://wooordhunt.ru' + '%20'.join(p.find('a')['href'].split()))
        for i in get_url(words_links):
            i


all_links(vocab)
