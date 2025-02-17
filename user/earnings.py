from user.format import FormattableValue


class Ferma:
	def __init__(self):
		self.balance = FormattableValue('balance', 'ferma')
		self.nalogs = FormattableValue('nalogs', 'ferma')
		self.cards = FormattableValue('cards', 'ferma')
		
	def update_data(self, data):
		self.balance.set(data[1], data[0])
		self.nalogs.set(data[2], data[0])
		self.cards.set(data[3], data[0])


class Business:
	def __init__(self):
		self.balance = FormattableValue('balance', 'business')
		self.nalogs = FormattableValue('nalogs', 'business')
		self.territory = FormattableValue('territory', 'business')
		self.bsterritory = FormattableValue('bsterritory', 'business')
	
	def update_data(self, data):
		self.balance.set(data[1], data[0])
		self.nalogs.set(data[2], data[0])
		self.territory.set(data[3], data[0])
		self.bsterritory.set(data[4], data[0])


class Garden:
	def __init__(self):
		self.balance = FormattableValue('balance', 'garden')
		self.nalogs = FormattableValue('nalogs', 'garden')
		self.tree = FormattableValue('tree', 'garden')
		self.water = FormattableValue('water', 'garden')
	
	def update_data(self, data):
		self.balance.set(data[1], data[0])
		self.nalogs.set(data[2], data[0])
		self.tree.set(data[3], data[0])
		self.water.set(data[4], data[0])


class Generator:
	def __init__(self):
		self.balance = FormattableValue('balance', 'generator')
		self.nalogs = FormattableValue('nalogs', 'generator')
		self.turbine = FormattableValue('turbine', 'generator')
	
	def update_data(self, data):
		self.balance.set(data[1], data[0])
		self.nalogs.set(data[2], data[0])
		self.turbine.set(data[3], data[0])


class Quarry:
	def __init__(self):
		self.balance = FormattableValue('balance', 'quarry')
		self.nalogs = FormattableValue('nalogs', 'quarry')
		self.territory = FormattableValue('territory', 'quarry')
		self.bur = FormattableValue('bur', 'quarry')
		self.lvl = FormattableValue('lvl', 'quarry')
	
	def update_data(self, data):
		self.balance.set(data[1], data[0])
		self.nalogs.set(data[2], data[0])
		self.territory.set(data[3], data[0])
		self.bur.set(data[4], data[0])
		self.lvl.set(data[5], data[0])


class Tree:
	def __init__(self):
		self.balance = FormattableValue('balance', 'quarry')
		self.nalogs = FormattableValue('nalogs', 'quarry')
		self.territory = FormattableValue('territory', 'quarry')
		self.tree = FormattableValue('tree', 'quarry')
		self.yen = FormattableValue('yen', 'quarry')
	
	def update_data(self, data):
		self.balance.set(data[1], data[0])
		self.nalogs.set(data[2], data[0])
		self.territory.set(data[3], data[0])
		self.tree.set(data[4], data[0])
		self.yen.set(data[5], data[0])
