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

link = f'https://api.hh.ru/vacancies?text=Name%3A%28data+analyst+or+data+or+%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%29+and+DESCRIPTION%3A%28numpy%29+NOT+Engineer+NOT+%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D1%80+NOT+Senior+not+%D0%9F%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8C+NOT+TechLead+NOT+%D1%82%D0%B5%D1%85%D0%BB%D0%B8%D0%B4&per_page=100'


def get_vacancies_id(url):
    vacancies = []
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    pages = data['pages']
    for page in range(pages):
        print(f'я должен обрабатываю страницу – {page}')
        response = requests.get(url, headers=headers, params={'page': page})
        data = json.loads(response.text)
        print(data['page'])
        clear_data = data['items']
        for i in clear_data:
            vacancies.append(i['id'])
    return vacancies


a = get_vacancies_id(link)
print(a)
print(Counter(a))

