import operator

class ObjectList(list):
	def __getitem__(self, item):
		attr = list.__getitem__(self, item)
		if type(attr) == dict:
			return Object(attr)
		elif type(attr) == list:
			return ObjectList(attr)
		return attr

class Object(dict):
	def __getitem__(self, item):
		try:
			attr = dict.__getitem__(self, item)
		except:
			return None
		if type(attr) == dict:
			return Object(attr)
		elif type(attr) == list:
			return ObjectList(attr)
		return attr

	def __getattr__(self, attr):
		attr = self[attr]
		return attr

	def getAttr(self, attr):
		try:
			return operator.attrgetter(attr)(self)
		except:
			return False