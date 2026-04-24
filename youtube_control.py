from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

def play_youtube(song):
    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.youtube.com")
    time.sleep(2)

    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys(song)
    search_box.send_keys(Keys.RETURN)

    time.sleep(3)

    video = driver.find_element(By.ID, "video-title")
    video.click()