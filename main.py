import time
import pdb
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


driver = webdriver.Chrome()  # Optional argument, if not specified will search path.

driver.get('https://www.facebook.com')

cookies = [
    # add cookies here
    # TODO: should use json or txt to load cookies
]

for cookie in cookies:
    driver.add_cookie(cookie)


driver.get('https://www.facebook.com') # facebook post here

#driver.refresh()
actions = ActionChains(driver)

csv_filename = "facebook_comments.csv"
csv_file = open(csv_filename, "w", newline="", encoding="utf-8")
writer = csv.writer(csv_file)

writer.writerow(["Author", "Comment"])

time.sleep(5) # Let the user actually see something!

def read_comment(comment):
    # pdb.set_trace()
    container = comment.find_element(By.XPATH, "./ancestor::li")
    actions.move_to_element(comment).perform()
    text = comment.find_element(By.CSS_SELECTOR, "[lang]").text
    author = comment.find_element(By.CSS_SELECTOR, "a[role='link'][tabindex='0']").text
    data = [author, text]
    writer.writerow(data)

    children = container.find_elements(By.XPATH, './*')

    if (len(children) > 1):
        open_button = children[1].find_element(By.CSS_SELECTOR, '[role=button]')
        actions.move_to_element(open_button).perform()
        open_button.click()


        comments_thread = children[1].find_elements(By.CSS_SELECTOR, 'ul > li div[role=article]')
        # pdb.set_trace()
        read_comments(comments_thread)


def read_comments(comments):
    for comment in comments:
        read_comment(comment)


def main():
    comments = driver.find_elements(By.CSS_SELECTOR, 'div[role=article] ul > li div[role=article]')
    read_comments(comments)

main()

time.sleep(5) # Let the user actually see something!

driver.quit()

print(f"CSV file '{csv_filename}' created successfully.")
