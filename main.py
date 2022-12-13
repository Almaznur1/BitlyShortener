import requests
import argparse
import os
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(url, headers):
    body = {"long_url": url}
    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten',
        headers=headers,
        json=body
    )
    response.raise_for_status()
    return response.json()['link']


def count_clicks(bitlink, headers):
    url_parts = urlparse(bitlink)
    link = f'{url_parts.netloc}{url_parts.path}'
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary',
        headers=headers
    )
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(url, headers):
    url_parts = urlparse(url)
    link = f'{url_parts.netloc}{url_parts.path}'
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{link}',
        headers=headers
    )
    return response.ok


def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    url = parser.parse_args().url
    token = os.environ["BITLY_TOKEN"]
    headers = {"Authorization": f"Bearer {token}"}
    try:
        if is_bitlink(url, headers):
            print('Переходов по ссылке всего:', count_clicks(url, headers))
        else:
            print('Битлинк:', shorten_link(url, headers))
    except requests.exceptions.HTTPError:
        print('введен неправильный битлинк или URL для сокращения')


if __name__ == "__main__":
    main()
