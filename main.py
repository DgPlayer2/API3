import os
import requests
from urllib.parse import urlparse


def shorten_link(token, long_url):
    url = "https://api.vk.ru/method/utils.getShortLink"
    params = {"v": "5.199", "access_token": token, "url": long_url}
    response = requests.post(url, params=params)
    response.raise_for_status()

    if "response" not in response.json():
        raise KeyError("Отсутствует ключ 'response' в ответе от API")

    if "error" in response.json():
        raise ValueError(f"Ошибка VK API: {response.json()['error']['error_msg']}")

    return response.json()["response"]["short_url"]


def count_clicks(token, short_link):
    url = "https://api.vk.ru/method/utils.getLinkStats"
    params = {
        "key": short_link,
        "v": "5.256",
        "access_token": token,
        "interval": "forever",
        "extended": 0,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    if "response" not in response.json():
        raise KeyError("Отсутствует ключ 'response' в ответе от API")
    
    if "error" in response.json():
        raise ValueError(f"Ошибка VK API: {response.json()['error']['error_msg']}")
        
    return response.json()["response"]["stats"]
    

def is_short_link(link, token):
    url = "https://api.vk.ru/method/utils.checkLink"
    params = {"url": link, "v": "5.199", "access_token": token}
    response = requests.get(url, params=params)
    response.raise_for_status()

    if 'error' in response.json():
        raise ValueError(f"VK API Ошибка: {response.json()['error']['error_msg']}")
        
    return response.json()["response"]['stats']


def main():
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    parser = argparse.ArgumentParser(description='Этот скрипт сокращает ссылки')
    parser.add_argument('link', help='Введите ссылку:')
    args = parser.parse_args()
    long_url = args.link
    
    if "response" not in response.json():
        raise KeyError("Отсутствует ключ 'response' в ответе от API")

    if "error" in response.json():
        raise ValueError(f"Ошибка VK API: {response.json()['error']['error_msg']}")

    return response.json()["response"]["status"] == "not_banned"


def main():
    vk_token = os.environ['VK_TOKEN']
    user_link = input("Введите ссылку: ")
    try:
        if is_short_link(user_link, vk_token):
            short_path = urlparse(user_link).path.lstrip("/")
            print(f"Количество кликов по ссылке: {count_clicks(vk_token, short_path)[0]['views']}")
        else:
            short_url = shorten_link(vk_token, user_link)
            print(f"Сокращённая ссылка: {short_url}")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP ошибка: {e}")
    except KeyError as e:
        print(f"Ошибка данных: {e}")


if __name__ == "__main__":
    main()
