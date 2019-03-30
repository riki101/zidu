# -*- coding: utf-8 -*-

"""
	-----------------------------
		Copyright - 2018
		Samuele Tolomeo 
		USAGE PERMISSION ONLY
	-----------------------------
"""

import json, requests, threading
from .Object import Object

class Bot:
	def __init__(self, token):
		self.token = token
		self.API = "https://api.telegram.org/bot%s/" % token # Pre-formatted API url
		self.session = requests.Session() # A session is faster than normal requests
		self.__handlers = []
		self.__nsh = {}

	def handle(self, attribute=None, value=None, startsWith=False):
		def addToHandlers(function):
			self.__handlers.append({
				"function": function,
				"attribute": attribute,
				"value": value,
				"startsWith": startsWith
			})
		return addToHandlers

	def req(self, res, **kwargs):
		return self.session.post(
			self.API + res,
			**kwargs
		).json()

	def polling(self):
		offset = 0
		while True:
			update = self.req(
				"getUpdates",
				data={
					"offset": offset
				}
			)
			update = Object(update)
			if update['ok'] == False:
				raise Exception(update['description'])
			if not len(update['result']) > 0:
				continue
			result = update['result'][0]
			offset = result['update_id']+1
			message = result['message']
			if not message:
				continue
			message['user'] = message.pop("from")
			for handler in self.__handlers:
				attr = message.getAttr(handler['attribute'])
				if attr != False:
					if attr == handler['value'] or (attr != False and attr.startswith(handler['value']) and self.__handlers['startsWith']):
						threading.Thread(target=handler['function'], args=[message]).start()
				else:
					threading.Thread(target=handler['function'], args=[message]).start()