from status import Status
from send import Send

import schedule
import time
import serial

import json

with open("config.json") as file:
    json_data = json.load(file)


def job():
    status.get_groups_handler()
    status.format_link()

    status.run()

    send.send_string(status.display_result())

# def updateGroup():


status = Status(json_data["url"], json_data["groups"]["groups_num"])
status.get_groups_handler()
status.format_link()

status.run()
status.display_result()

send = Send(json_data["serial"]["interface"], json_data["serial"]["baud_rate"])
# send = Send(json_data["serial"]["interface"], json_data["serial"]["baud_rate"])


schedule.every(1).seconds.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)


send.close()
