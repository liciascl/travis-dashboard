from status import Status
import schedule
import time
import serial


import json

with open("config.json") as file:
    json_data = json.load(file)


if("url" not in json_data):
    print("Url not defined, insert in config.json")
    quit()


def job():
    status.run()
    status.print_all()


status = Status(json_data["url"])
status.get_groups_handler()
status.format_link()

status.run()
status.print_all()


schedule.every(5).seconds.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
