import time
from bs4 import BeautifulSoup
import urllib.request as requests


class Status:

    def __init__(self, url):
        self.url = url
        self.groups = {}
        self.groups_url = None

    def get_groups(self):
        response = requests.urlopen(self.url)
        html_csv = response.read().decode("utf-8")
        html_csv = html_csv.split("\r\n")

        self.groups_url = html_csv[1:]  # Retira a Primeira linha da tabela

    def format_link(self):

        for lines in self.groups_url:
            a = lines.split(",")
            try:
                if(len(a[1]) > 0):
                    self.groups[a[0]] = {}
                    if a[1][-1] == "/":
                        a[1] = a[1][:-1]
                    link = "https://travis-ci.org" + a[1].split("github.com")[1] + ".svg?branch=master"

                    self.groups[a[0]]["link"] = link

            except:
                print("Link not valid")

    def get_travis_status(self):

        for group in self.groups:
            words = []
            response = requests.urlopen(self.groups[group]["link"])
            html = response.read()
            soup = BeautifulSoup(html, features="html5lib")
            for text_tags in soup.find_all('text'):
                if str(text_tags.text) not in words:
                    words.append(str(text_tags.text))

            self.groups[group]["words"] = words


if __name__ == "__main__":
    status = Status("https://docs.google.com/spreadsheets/d/1oK-7ITXBQ40BhHO-izAtLTZBzcwrWoWWmYKwCIP9Z_g/export?format=csv")
    status.get_groups()
    status.format_link()
    status.get_travis_status()
    pass
