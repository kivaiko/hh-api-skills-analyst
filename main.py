import requests
import json
import re
import bleach
from collections import Counter
from filter import words_filter
from conf import HEADERS


""" Поисковы запрос на HH.Важно! Иногда hh добавляет в запрос параметр "&salary=",
нужно убрать его иначе api не будет отдавать данные
"""
search_url = 'https://hh.ru/search/vacancy?text=Name%3A%28python+or+django+or+drf+or+backend+or+fastapi+or+flask%29+and+DESCRIPTION%3A%28django+or+drf+or+fastapi+or+flask%29+NOT+%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D1%80+NOT+Senior+not+%D0%9F%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8C+NOT+TechLead+NOT+%D1%82%D0%B5%D1%85%D0%BB%D0%B8%D0%B4'


""" Сколько оставь слов в итоговой выборке """
values_in_top = 100


def get_link(url):
    print('Start – get_link')
    url = url[29:]
    search_link = f'https://api.hh.ru/vacancies?{url}&per_page=100'
    return search_link


def get_vacancies_id(url):
    print('Start – get_vacancies_id')
    vacancies_ids = []
    response = requests.get(url, headers=HEADERS)
    data = json.loads(response.text)
    pages = data['pages']
    for page in range(pages):
        response = requests.get(url, headers=HEADERS, params={'page': page})
        data = json.loads(response.text)
        clear_data = data['items']
        for i in clear_data:
            vacancies_ids.append(i['id'])
    return vacancies_ids


def get_skills_from_id(data):
    skills_for_id = []
    for skill in data:
        skills_for_id.append(skill['name'])
    return skills_for_id


def get_keywords_from_id(data):
    vacancies_description = ''
    txt = bleach.clean(data, tags=[], strip=True)
    txt = re.findall(r'[A-Za-z0-9]+', txt)
    txt = ' '.join(txt)
    txt = txt.lower()
    vacancies_description += txt
    words_list = clean(vacancies_description)
    return words_list


def get_data_from_vacancies_id(ids):
    print('Start – get_data_from_vacancies_id')
    skills_list = []
    keywords_list = []
    for vacancy_id in ids:
        print(vacancy_id)
        response = requests.get('https://api.hh.ru/vacancies/' + vacancy_id, headers=HEADERS)
        data = json.loads(response.text)
        skills_list += get_skills_from_id(data['key_skills'])
        keywords_list += get_keywords_from_id(data['description'])
    return skills_list, keywords_list


def clean(txt):
    all_words = []
    for word in txt.split():
        all_words.append(word)
    new_list = [item for item in all_words if item not in words_filter]
    return new_list


def count_words(url):
    link = get_link(url)
    vacancies_ids = get_vacancies_id(link)
    skills, keywords = get_data_from_vacancies_id(vacancies_ids)
    print(Counter(skills).most_common(values_in_top))
    print(' ')
    print(Counter(keywords).most_common(values_in_top))


count_words(search_url)
