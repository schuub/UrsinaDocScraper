from bs4 import BeautifulSoup
# import requests


if __name__ == "__main__":
    with open("ursina_cheat_sheet.html") as file:
        soup = BeautifulSoup(file, 'html5lib')

    docs = dict()

    content = soup.find('div', id='content') \
        .find_all('div', recursive=False)

    for e in content[48:50]:
        search_string = e.div['id'].lower()
        res = {
            'title': e.div.text,
            'github_url': e.contents[1].a['href'],
            'example': "test",
        }
        print(search_string)
        print(e.contents[1].a['href'])
        print()
        docs[search_string] = res

    print(docs['vec3']['github_url'])