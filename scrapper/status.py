import json
import asyncio
import aiohttp


class Status:

    def __init__(self, url, groups_num):
        self.url = url
        self.groups = {}
        self.groups_url = None
        self.groups_num = groups_num

    def get_groups_handler(self):
        asyncio.get_event_loop().run_until_complete(self.get_groups())

    async def get_groups(self):
        self.groups = {}
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
            self.groups[group]["content"] = json.loads(await response.text())

    async def download_all_sites(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for group in self.groups:
                task = asyncio.ensure_future(self.download_site(session, self.groups[group]["link"], group))
                tasks.append(task)
            await asyncio.gather(*tasks, return_exceptions=True)

    def mapStatus(self, status):
        if(status == None):
            return "B"
        elif(status == 0):
            return "G"
        elif(status == 1):
            return "R"
        else:
            print("Status not found", status)
            return "B"

    def result_from_content(self, group):
        if(len(self.groups[group]["content"]) == 0):
            return None
        else:
            return self.groups[group]["content"][0]["result"]

    def display_result(self):
        data = ""
        entries = list(self.groups.keys())
        if len(entries) == 0:
            data = "B"*self.groups_num

        # Se tiver apenas um grupo colocar o painel inteiro
        elif (len(entries) == 1):
            data = (self.mapStatus(self.result_from_content(entries[0])))*(self.groups_num)
        else:
            for group in self.groups:
                data += (self.mapStatus(self.result_from_content(group)))

        size = len(data)
        if(size < self.groups_num):
            data += "B"*(self.groups_num-size)
        print(data)
        return data

    def run(self):

        asyncio.get_event_loop().run_until_complete(self.download_all_sites())
