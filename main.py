import re
from bs4 import BeautifulSoup
# import requests


if __name__ == "__main__":
    with open("html/ursina_cheat_sheet.html") as file:
        soup = BeautifulSoup(file, 'html5lib')

    docs = dict()

    content = soup.find('div', id='content') \
        .find_all('div', recursive=False)

    for e in content[50:51]:
        info = e.contents[1]
        search_string = e.div['id'].lower()
        example = info.find('div', class_='example').extract()

        regex = re.compile(r'(?:\n)([a-z_A-Z]+\(.*\))')
        methods = regex.findall(info.text)
        res = {
            'title': e.div.text,
            'github_url': info.a['href'],
            'example': example.text,
            'params': info.find('params').text,
            'methods': methods,
        }
        docs[search_string] = res

    print(docs['animation']['methods'])
