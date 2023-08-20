import os
import csv
import json
import pdb
import time

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

FB_URL = os.getenv('FB_URL') or 'https://www.facebook.com/jhonfeiber/posts/pfbid0UKjbWuMtv1rTcuuUuD6VRJpKeoUeZHipU1E7889pspkB6ujgdq4MAPaNpHpPC6CSl'

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.

driver.get('https://www.facebook.com')

with open('cookies.json') as cookies_file:
  cookies = cookies_file.read()

cookies = json.loads(cookies)

for cookie in cookies:
    driver.add_cookie(cookie)

driver.get(FB_URL) # facebook post here

#driver.refresh()
actions = ActionChains(driver)


current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
csv_filename = f"comments/{current_time}.csv"
csv_file = open(csv_filename, "w", newline="", encoding="utf-8")
writer = csv.writer(csv_file)

writer.writerow(["Author", "Comment"])

time.sleep(5) # Let the user actually see something!

def read_comment(comment, nested = False):
    actions.move_to_element(comment).perform()

    try:
        see_more = comment.find_element(By.XPATH, ".//div[@role='button'][text()='Ver más']")
        see_more.click() if see_more else None
    except (NoSuchElementException, AttributeError):
        None

    try:
        text = comment.find_element(By.CSS_SELECTOR, "[lang]").text
        author = comment.find_element(By.CSS_SELECTOR, "a[role='link'][tabindex='0']").text

        data = [author, text]
        writer.writerow(data)

        thread = comment.find_element(By.XPATH, "../../div[2]")

        if thread is not None and nested is not False:
            open_button = thread.find_element(By.XPATH, ".//div[@role='button'][@tabindex='0']")
            actions.move_to_element(open_button).perform()
            open_button.click()

            comments_thread = thread.find_elements(By.CSS_SELECTOR, 'ul > li div[role=article]')
            for comment_thread in comments_thread:  # Iterate through comments_thread
                time.sleep(1) # Let the user actually see something!
                read_comment(comment_thread)

    except NoSuchElementException:
        pass


def main():
    comments = driver.find_elements(By.CSS_SELECTOR, 'div[role=article] ul > li div[role=article]')
    for comment in comments:
        read_comment(comment, True)

main()

time.sleep(5) # Let the user actually see something!

driver.quit()

print(f"CSV file '{csv_filename}' created successfully.")

