import requests


def load_html(url) -> str:
    url = requests.get(url)
    htmltext = url.text
    return htmltext
