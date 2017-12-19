from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from sendemail import send_mail
import time
import os
import sys
import config

def download_files():
    thisPath = os.path.split(os.path.abspath(sys.argv[0]))[0] + "/"
    files = []

    url = 'https://reg.usps.com/portal/login?app=RMIN&appURL=https%3A%2F%2Finformeddelivery.usps.com%2Fbox%2Fpages%2Fintro%2Fstart.action%3Frestart%3D1'

    display = Display(visible=0, size=(800, 600))
    display.start()

    browser = webdriver.Chrome()
    browser.get(url)

    username = browser.find_element_by_name('username')
    username.send_keys(config.MYUSPS_USERNAME)

    password = browser.find_element_by_name('password')
    password.send_keys(config.MYUSPS_PASSWORD)

    browser.find_element_by_id('btn-submit').click()

    time.sleep(20)
    html = browser.page_source

    soup = BeautifulSoup(html, 'lxml')

    todaysMail = soup.findAll('div', { 'class': 'mailpieceBox' })

    if todaysMail:
        for mail in todaysMail:
            img_src = mail.find("img")["src"]
            image_url = "https://informeddelivery.usps.com/box/pages/secure/" + img_src
            browser.get(image_url)
            browser.save_screenshot(thisPath + img_src.split("=", 1)[1] + ".png")
            files.append(thisPath + img_src.split("=", 1)[1] + ".png")

    browser.quit()
    display.stop()

    return files
