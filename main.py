from selenium import webdriver
from selenium.webdriver.common.by import By

from time import sleep
import pickle

import config


options = webdriver.EdgeOptions()


class Request:
	def __init__(self, url, info):
		self.browser = webdriver.Edge(options=options)
		self.browser.get(url)
		sleep(100)

		self.url = url

		info = info.replace('(', '').replace(')', '').split()
		self.TYPE = info[0]
		self.total = ''
		self.value = ''

		if self.TYPE in ['O', 'U']:
			self.total = info[1]
			self.value = info[2]
		else:
			self.value = info[1]

		print("[LOG] TYPE", self.TYPE, "| Total:", self.total, "| Value:", self.value)


	def authorization(self):
		for cookie in pickle.load(open("session", "rb")):
			self.browser.add_cookie(cookie)

		self.browser.refresh()
		sleep(10)


	def set_bet(self):
		sections = self.browser.find_elements(By.CLASS_NAME, "odds-type-section")

		for secs in sections:
			print("[LOG] foring cols")
			if self.TYPE in ['O', 'U']:
				if secs.get_attribute("data-odds-type-id") != "10_null": continue
				print("[LOG] found totals")

				for btn in secs.find_elements(By.CLASS_NAME, "match-odd"):
					info = btn.find_element(By.CLASS_NAME, "odd-name").text.strip().split()

					if self.total != info[0] or info[1] != ('М' if self.TYPE == 'U' else 'Б'):
						continue

					print("[LOG] total found")
					btn.click()
					return True

			elif self.TYPE in ['1', '2', 'X']:
				if secs.get_attribute("data-odds-type-id") != "1_null": continue
				print("[LOG] found 1x2")

				for btn in secs.find_elements(By.CLASS_NAME, "match-odd"):
					if self.TYPE not in btn.find_element(By.CLASS_NAME, "odd-name").text.strip():
						continue

					print("[LOG] clicked 1x2")
					btn.click()
					return True


	def confirm_bet(self):
		coupon = self.browser.find_element(By.CLASS_NAME, "coupon")

		coef = coupon.find_element(By.CLASS_NAME, "BaseCouponOdd_coefficient_oUrpy")
		amount = coupon.find_element(By.CLASS_NAME, "amount-input")
		submit = coupon.find_element(By.CLASS_NAME, "base-coupon-submit")

		# if self.value != coef.text:
		#	return False

		amount.send_keys("10")

		return True

		# submit.click()


	def exit(self):
		self.browser.quit()
		self.browser.close()



"""
dolbojebina@gmail.com
Nikitos222!


https://1wpyun.xyz/bets/prematch/23/220/5496/15492594  —> U 143.5 (1.97)
https://1wpyun.xyz/bets/prematch/18/144/875/15474381  —> O 3.5 (2.25)

https://1wpyun.xyz/bets/prematch/18/144/1045/15381160  —> X (4.4)
https://1wpyun.xyz/bets/prematch/23/220/5496/15475027  —> 1 (1.39)
https://1wpyun.xyz/bets/prematch/18/160/3823/15424288  —> 2 (3.9)
"""