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


search_url = 'https://hh.ru/search/vacancy?employment=part&experience=between3And6&search_field=name&search_field=company_name&search_field=description&text=python+backend&ored_clusters=true&enable_snippets=true&L_save_area=true'


def get_link(url):
    url = url[29:]
    link = f'https://api.hh.ru/vacancies?{url}&per_page=100'
    return link


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


link = get_link(search_url)
vacancies_ids = get_vacancies_id(link)
keywords = get_keywords(vacancies_ids)
skills = get_skills(vacancies_ids)


print(Counter(keywords).most_common(100))




