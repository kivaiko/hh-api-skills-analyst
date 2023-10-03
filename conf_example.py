# Данные от hh
CLIENT_ID = 'example'
CLIENT_SECRET = 'example'
ACCESS_TOKEN = 'example'
EMAIL = 'email'
APP_NAME = 'name'

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': f'{APP_NAME} ({EMAIL})',
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}