from bs4 import BeautifulSoup
# import requests


class Entry():
    def __init__(self):
        self.title = ""
        self.github_url = ""
        self.attributes = []
        self.example = ""


if __name__ == "__main__":
    with open("ursina_cheat_sheet.html") as file:
        soup = BeautifulSoup(file, 'html5lib')

    match = soup.find('div', id='content').div
    entry = match.div
    print(entry)
