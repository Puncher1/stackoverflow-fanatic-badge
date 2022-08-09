import os
import time
import re

import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

import mail_support
from sel_driver import SeleniumDriver


def login():
    email = os.getenv("STACKOVERFLOW_EMAIL")
    password = os.getenv("STACKOVERFLOW_PW")
    display_name = os.getenv("STACKOVERFLOW_DISPLAY_NAME")

    driver = SeleniumDriver(options=["--no-sandbox", "--headless", "--disable-gpu", "--disable-dev-shm-usage"]).driver
    try:
        driver.get("https://stackoverflow.com")

        driver.find_element(By.LINK_TEXT, "Log in").click()
        time.sleep(1)

        driver.find_element(By.ID, "email").send_keys(email)
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys(password)
        time.sleep(1)
        driver.find_element(By.ID, "submit-button").submit()
        time.sleep(1)

        # Human Verification check
        try:
            driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div[2]/h1')
        except selenium.common.NoSuchElementException:
            pass
        else:
            mail_support.send_error("Human Verification!")
            return

        time.sleep(1)

        # profile button
        driver.find_element(By.XPATH, "/html/body/header/div/ol[2]/li[2]/a").click()
        time.sleep(1)

        # display name
        elem = WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="mainbar-full"]/div[1]/div[1]/div/div/div[1]'))
        )
        assert display_name in elem.text
        time.sleep(1)

        visit_text = driver.find_element(By.XPATH, '//*[@id="js-daily-access-calendar-container"]/button/div[2]').text
        login_streak = re.findall("\d+", visit_text)[1]

        mail_support.send_passed(login_streak)

    except Exception as e:
        mail_support.send_error(e.__class__.__name__)

    finally:
        driver.close()
