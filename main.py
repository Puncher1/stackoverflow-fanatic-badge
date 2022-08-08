from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

import stackoverflow


load_dotenv()
schedule = BlockingScheduler()


@schedule.scheduled_job("interval", minutes=1)
def access_stackoverflow_page():
    stackoverflow.login()


if __name__ == "__main__":
    schedule.start()
