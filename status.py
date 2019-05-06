import time
from bs4 import BeautifulSoup
import requests

import json
import asyncio
import aiohttp


class Status:

    def __init__(self, url):
        self.url = url
        self.groups = {}
        self.groups_url = None

    def get_groups(self):
        response = requests.get(self.url)

        data = response.text.split("\r\n")
        self.groups_url = data[1:]  # Retira a Primeira linha da tabela

    def format_link(self):

        for lines in self.groups_url:
            a = lines.split(",")

            if(len(a[1]) > 0):
                if a[1][-1] == "/":
                    a[1] = a[1][:-1]
                link = "https://api.travis-ci.org/repos" + a[1].split("github.com")[1]+"/builds"

                self.groups[a[0]] = {}
                self.groups[a[0]]["link"] = link

    # def get_travis_status(self):
    #     for group in self.groups:
    #         response = requests.get(self.groups[group]["link"])

    async def download_site(self, session, url, group):
        async with session.get(url) as response:
            self.groups[group]["content"] = await response.text()

    async def download_all_sites(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for group in self.groups:
                task = asyncio.ensure_future(self.download_site(session, self.groups[group]["link"], group))
                tasks.append(task)
            await asyncio.gather(*tasks, return_exceptions=True)

    def print_all(self):
        for group in self.groups:

            print(group, json.loads(self.groups[group]["content"])[0]["result"])

    def run(self):

        asyncio.get_event_loop().run_until_complete(self.download_all_sites())
        # duration = time.time() - start_time
        # print("Downloaded sites in {0} seconds".format(duration))


#
if __name__ == "__main__":
    status = Status("https://docs.google.com/spreadsheets/d/1oK-7ITXBQ40BhHO-izAtLTZBzcwrWoWWmYKwCIP9Z_g/export?format=csv")
    status.get_groups()
    status.format_link()
    status.run()
    status.print_all()

    # pass


# GET https: // api.travis-ci.org/repos/xxxx/yyy/builds
