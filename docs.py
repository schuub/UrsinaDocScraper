import datetime
import re
import requests
from bs4 import BeautifulSoup

CHEAT_SHEET_URL = "https://www.ursinaengine.org/cheat_sheet_dark.html"
# Time before cached version will be updated (in seconds)
MAX_DATA_AGE = 1800


class CheatSheet():
    """ Use get_doc(keyword) for queries."""

    def __init__(self, local_html=None) -> None:
        self.last_update = datetime.datetime.now()
        self.__html = ""
        self.docs = dict()
        if local_html:
            with open(local_html) as file:
                self.__html = file.read()
        self.__fetch_from_url(CHEAT_SHEET_URL)
        self.__parse_html()

    def get_doc(self, keyword: str) -> dict:
        """ Retrieve a dictionary containing cheat sheet 
        information for a given keyword"""
        if self.check_data_expired():
            self.__fetch_from_url(CHEAT_SHEET_URL)
            self.__parse_html()

        res = self.docs.get(keyword)
        return res or {}

    def get_keys(self) -> list:
        return sorted(self.docs.keys())

    def __fetch_from_url(self, url: str) -> bool:
        print(f"GET: {CHEAT_SHEET_URL}")
        response = requests.get(url)
        if response.ok:
            print("response OK")
            self.last_update = datetime.datetime.now()
            self.__html = response.text
            return True
        else:
            print("Error while fetching HTML: Invalid response from",
                  CHEAT_SHEET_URL,
                  "Using local version if available.")
            return False

    def check_data_expired(self) -> bool:
        time_delta = (datetime.datetime.now() - self.last_update).seconds
        if time_delta > MAX_DATA_AGE:
            return True
        else:
            return False

    def __parse_html(self) -> None:
        soup = BeautifulSoup(self.__html, "html5lib")
        content = soup.find("div", id="content").find_all(
            "div", recursive=False)

        for e in content[50:51]:
            info = e.contents[1]
            search_string = e.div["id"].lower()
            example = info.find("div", class_="example").extract()

            regex = re.compile(r"(?:\n)([a-z_A-Z]+\(.*\))")
            methods = regex.findall(info.text)
            res = {
                "label": e.div.text,
                "github_url": info.a["href"],
                "example": example.text,
                "params": info.find("params").text,
                "methods": methods,
            }
            self.__set_key(search_string, res)

    def __set_key(self, key: str, value: dict) -> None:
        self.docs[key] = value


if __name__ == "__main__":
    from pprint import PrettyPrinter
    pp = PrettyPrinter()
    cs = CheatSheet()
    # cs = CheatSheet(local_html="test_data/ursina_cheat_sheet.html")

    pp.pprint(cs.get_doc("animation"))
