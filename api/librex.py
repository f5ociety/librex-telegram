import requests
from config import LIBREX_INSTANT_URL

url = "https://" + LIBREX_INSTANT_URL + "/api.php?q={}&p={}&t=0"


def request(query, page=0):
    """Отправка запроса на linrex API

    Args:
        query (string): Строка запроса для поиска в librex
        page (int, optional): Номер страницы для поиска. Defaults to 0.

    Returns:
        json: Массив json из 9 ответов

    Returns's example:
    [
        {
            "title": "Handbook: Главная страница - Gentoo Wiki",
            "url": "https://wiki.gentoo.org/wiki/Handbook:Main_Page/ru",
            "base_url": "https://wiki.gentoo.org/",
            "description": "9 нояб. 2021 г. — Руководство Gentoo — это результат деятельности ..."
        },
        {
            "title": "Gentoo на нетбуке, философия самоограничения и ... - Habr",
            "url": "https://habr.com/ru/post/702172/",
            "base_url": "https://habr.com/",
            "description": "28 нояб. 2022 г. — В 2022 году Gentoo Linux по-прежнему ..."
        }, ...
    ]
    """
    resp = requests.get(url=url.format(query, page), timeout=5)
    data = resp.json()
    return data
