from apscheduler.schedulers.blocking import BlockingScheduler

import stackoverflow


schedule = BlockingScheduler()

@schedule.scheduled_job("interval", hours=12)
def access_stackoverflow_page():
    stackoverflow.login()


if __name__ == "__main__":
    schedule.start()
