from selenium import webdriver

import pickle
import time


browser = webdriver.Edge()

try:
	browser.get("https://1wpyun.xyz/bets/home")

	time.sleep(100)

	for cookie in pickle.load(open("session", "rb")):
		browser.add_cookie(cookie)

	browser.refresh()

	time.sleep(300)

except Exception:
	browser.quit()
	browser.close()