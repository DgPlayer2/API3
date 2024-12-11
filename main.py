import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(vk_token, long_url):
    params = {"v": "5.199", "url": long_url}
    headers = {"Authorization": f"Bearer {vk_token}"} 
    url = 'https://api.vk.com/method/utils.getShortLink'
    response = requests.post(url, params=params, headers=headers)
    response.raise_for_status()
    
    return response.json()["response"]["short_url"]
    

def count_clicks(vk_token, short_url_key):

    url = "https://api.vk.com/method/utils.getLinkStats"
    params = {
        "v": "5.236",
        "interval": "forever", 
        "extended": 0, 
        "key": short_url_key
    }    
    
    headers = {"Authorization": f"Bearer {vk_token}"} 
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    return response.json()["response"]['stats']


def is_shorten_link(long_url):
    parsed_url = urlparse(long_url)
    return parsed_url.netloc == "vk.cc"


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description='этот скрипт сокращает ссылки')
    parser.add_argument('link', help='Введите ссылку:')
    args = parser.parse_args()
    long_url = args.link
    vk_token = os.environ['VK_TOKEN']
    
    try:
        if is_shorten_link(long_url):
            short_url_key = long_url.split('/')[-1]
            statistics = count_clicks(vk_token, short_url_key)
            print(f"Количество кликов: {statistics[0]['views']}")
        else:
            short_link = shorten_link(vk_token, long_url)
            print(short_link) 
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка: {e}")
    
    
if __name__ == "__main__":
    main()