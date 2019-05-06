import json
import asyncio
import aiohttp


class Status:

    def __init__(self, url):
        self.url = url
        self.groups = {}
        self.groups_url = None

    def get_groups_handler(self):
        asyncio.get_event_loop().run_until_complete(self.get_groups())

    async def get_groups(self):

        async with aiohttp.request('GET', self.url) as resp:
            data = await resp.text()
        self.groups_url = data.split("\r\n")[1:]  # Retira a Primeira linha da tabela

    def format_link(self):

        for lines in self.groups_url:

            try:
                a = lines.split(",")

                if(len(a[1]) > 0):
                    if a[1][-1] == "/":
                        a[1] = a[1][:-1]
                    link = "https://api.travis-ci.org/repos" + a[1].split("github.com")[1]+"/builds"

                    self.groups[a[0]] = {}
                    self.groups[a[0]]["link"] = link
            except:
                print("Link not formated correctly")

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
