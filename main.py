import requests
import json
import re
from collections import Counter

CLIENT_ID = "GT11P1DLO4KP6OTSN0KQOQ4OA99KLPFAMRD4BJUKQ2RQS3SIA4COQEE738PRA5I7"
CLIENT_SECRET = "VQ2JNMG0579HOSRVD6M9B4TQLET5MN52M4R842QRVIETUNU549MI5DRHNKLFS9Q8"
ACCESS_TOKEN = "APPLPBBQB1CDN4DHJAPCSTR92M73395AU7RPU4K8LI6NSDDSUCFF87049KTUC9DR"
#  "token_type": "bearer"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'skill rating (alexagree1@gmail.com)',
    'Authorization': 'Bearer APPLPBBQB1CDN4DHJAPCSTR92M73395AU7RPU4K8LI6NSDDSUCFF87049KTUC9DR',
    'Content-Type': 'application/json'
}

link = f'https://api.hh.ru/vacancies?text=Name%3A%28python+or+django+or+drf+or+backend+or+fastapi+or+flask%29+and+DESCRIPTION%3A%28django+or+drf+or+fastapi+or+flask%29+NOT+%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D1%80+NOT+Senior+not+%D0%9F%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8C+NOT+TechLead+NOT+%D1%82%D0%B5%D1%85%D0%BB%D0%B8%D0%B4&per_page=100'


def get_vacancies_id(url):
    vacancies = []
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    pages = data['pages']
    for page in range(pages):
        response = requests.get(url, headers=headers, params={'page': page})
        data = json.loads(response.text)
        clear_data = data['items']
        for i in clear_data:
            vacancies.append(i['id'])
    return vacancies


def get_skills(ids):
    skills = []
    for vacancy_id in ids:
        response = requests.get('https://api.hh.ru/vacancies/' + vacancy_id, headers=headers)
        data = json.loads(response.text)
        for skill in data['key_skills']:
            skills.append(skill['name'])
    return skills


def get_keywords(ids):
    vacancies_description = ''
    for vacancy_id in ids:
        response = requests.get('https://api.hh.ru/vacancies/' + vacancy_id, headers=headers)
        data = json.loads(response.text)
        vacancies_description += data['description']
        words = clean(vacancies_description)
    return words


def clean(txt):
    words_list = []
    txt = txt.lower()
    cleaned_txt = re.sub(r'(\<(/?[^>]+)>)|[)(?«1.2•,:+!—;»3–⁃-]|[а-яё]|backend|&quot|(\\)', '', txt)
    for word in cleaned_txt.split():
        words_list.append(word)
    return words_list


vacancies_ids = get_vacancies_id(link)
keywords = get_keywords(vacancies_ids)

print(Counter(keywords).most_common(100))




