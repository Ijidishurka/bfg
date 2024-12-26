from user.format import FormattableValue


class Mine:
	def __init__(self):
		self.iron = FormattableValue('iron', 'mine')
		self.gold = FormattableValue('gold', 'mine')
		self.diamond = FormattableValue('diamond', 'mine')
		self.amestit = FormattableValue('amestit', 'mine')
		self.aquamarine = FormattableValue('aquamarine', 'mine')
		self.emeralds = FormattableValue('emeralds', 'mine')
		self.matter = FormattableValue('matter', 'mine')
		self.plasma = FormattableValue('plasma', 'mine')
		self.nickel = FormattableValue('nickel', 'mine')
		self.titanium = FormattableValue('titanium', 'mine')
		self.cobalt = FormattableValue('cobalt', 'mine')
		self.ectoplasm = FormattableValue('ectoplasm', 'mine')
		self.palladium = FormattableValue('palladium', 'mine')
	
	def update_data(self, mine):
		self.iron.set(mine[1], mine[0])
		self.gold.set(mine[2], mine[0])
		self.diamond.set(mine[3], mine[0])
		self.amestit.set(mine[4], mine[0])
		self.aquamarine.set(mine[5], mine[0])
		self.emeralds.set(mine[6], mine[0])
		self.matter.set(mine[7], mine[0])
		self.plasma.set(mine[8], mine[0])
		self.nickel.set(mine[9], mine[0])
		self.titanium.set(mine[10], mine[0])
		self.cobalt.set(mine[11], mine[0])
		self.ectoplasm.set(mine[12], mine[0])
		self.palladium.set(mine[14], mine[0])


class Property:
	def __init__(self):
		self.helicopter = FormattableValue('iron', 'mine')
		self.car = FormattableValue('gold', 'mine')
		self.yahta = FormattableValue('diamond', 'mine')
		self.phone = FormattableValue('amestit', 'mine')
		self.house = FormattableValue('aquamarine', 'mine')
		self.plane = FormattableValue('emeralds', 'mine')
	
	def update_data(self, property):
		self.helicopter.set(property[1], property[0])
		self.car.set(property[2], property[0])
		self.yahta.set(property[3], property[0])
		self.phone.set(property[4], property[0])
		self.house.set(property[5], property[0])
		self.plane.set(property[6], property[0])