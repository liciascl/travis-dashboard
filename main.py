from status import Status
import schedule
import time
import serial


def job():
    status.run()
    status.print_all()


status = Status("https://docs.google.com/spreadsheets/d/1oK-7ITXBQ40BhHO-izAtLTZBzcwrWoWWmYKwCIP9Z_g/export?format=csv")
status.get_groups()
status.format_link()

status.run()
status.print_all()


schedule.every(5).seconds.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
