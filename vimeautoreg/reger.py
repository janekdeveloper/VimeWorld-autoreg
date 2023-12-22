# -*- coding: utf8 -*-
"""
Author: @JanDeveloper
Version: 1.0.0
"""
import requests
from capmonster_python import RecaptchaV2Task
import secrets
import string
import json




class RegistrationRequest:
	def __init__(self, _client_key: str):
		self.captcha = RecaptchaV2Task(_client_key)
		self.s = requests.Session()
		self.website_url = "https://cp.vimeworld.com/register"
		self.data = {}
		self.passwords = ''

	def _captcha_solve(self):
		site_key = "6Lc35vYgAAAAAN-KKANPfYYt6des4ZS4ClD9bfQp"
		task_id = self.captcha.create_task(website_url=self.website_url, website_key=site_key)
		result = self.captcha.join_task_result(task_id=task_id)
		return result.get("gRecaptchaResponse")

	def _gen_nick(self, numlet):
		username_alphabet = string.ascii_letters
		while True:
			username = ''.join(secrets.choice(username_alphabet) for o in range(numlet))
			respn = requests.get(f"https://api.vimeworld.com/user/name/{username}") 
			if respn.json() == []:
				break
		return username

	def _gen_data(self, g_recaptcha, numlet: int, passlength: int):
		alphabet = string.ascii_letters + string.digits
		password = ''.join(secrets.choice(alphabet) for i in range(passlength))
		usernick = self._gen_nick(numlet)	
		self.payload = {
			'username': usernick,
			'password': password,
			'email': f'{password}@gmail.com',
			'recaptcha_response': g_recaptcha
		}
		self.passwords = f'{usernick}:{password}:{password}@gmail.com'

	def register_account(self, numlet: int = 8, passlength: int = 16):
		self._gen_data(g_recaptcha = self._captcha_solve(), numlet = numlet, passlength = passlength)
		response = self.s.post("https://cp.vimeworld.com/api/register", json = self.payload)
		respjson = response.json()
		if response.status_code in [200, 201]:
			return self.passwords#f'Логин: <code>{self.passwords.split(":")[0]}</code>\nПароль: <code>{self.passwords.split(":")[1]}</code>\n\nПочта: <code>{self.passwords.split(":")[2]}</code>\n\nДля использования бота снова, нажмите еще раз кнопку снизу'
		else:
			return respjson