import requests
from bs4 import BeautifulSoup
import time

url = 'https://www.bbc.com/amharic'
bot_token = '5965910148:AAEpBk69WW1Ux-kQ7poxMlHBtMIwrhscfKo'
bot_chat_id = '-1001962961885'

def scrape_data():
    data = []
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    paragraphs = soup.find_all('p')

    for paragraph in paragraphs:
        item = {}
        heading = paragraph.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if heading:
            heading_text = heading.get_text()
            item['heading'] = heading_text
        image = paragraph.find_previous('img')
        if image:
            image_url = image.get('src')
            item['image'] = image_url
        paragraph_text = paragraph.get_text()
        item['paragraph'] = paragraph_text
        data.append(item)
    return data

def post_to_telegram(data):
    for item in data:
        message = ""
        if 'heading' in item:
            message += f" {item['heading']}\n"
        if 'image' in item:
            message += f" {item['image']}\n"
        if 'paragraph' in item:
            message += f" {item['paragraph']}\n"
        base_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chat_id}&text={message}'
        requests.get(base_url)
        time.sleep(1)

while True:
    data = scrape_data()
    post_to_telegram(data)
    time.sleep(60)