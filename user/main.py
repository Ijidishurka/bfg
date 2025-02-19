from datetime import datetime

from commands import db
from user.format import FormattableValue

from user.earnings import Ferma, Business, Garden, Generator, Quarry, Tree
from user.other import Mine, Property
from user.clan import Clan


def get_text_status(status):
	status_dict = {0: "Обычный", 1: "Standart VIP", 2: "Gold VIP", 3: "Platinum VIP", 4: "Администратор"}
	return status_dict.get(status, status_dict[0])
	

class User:
	def __init__(self, message=None, call=None, not_class=None):
		self.message = message
		self.call = call
		self.user_id = None
		self.id = None
		self.not_class = not_class
		self.name = ''
		self.url = ''
		self.balance = FormattableValue('balance', big=True)
		self.btc = FormattableValue('btc', big=True)
		self.bank = FormattableValue('bank', big=True)
		self.depozit = FormattableValue('depozit', big=True)
		self.depozit_time = 0
		self.expe = FormattableValue('exp')
		self.energy = FormattableValue('energy')
		
		self.case = {
			1: FormattableValue('case1'),
			2: FormattableValue('case2'),
			3: FormattableValue('case3'),
			4: FormattableValue('case4')
		}
		
		self.rating = FormattableValue('rating')
		self.games = FormattableValue('games')
		self.bcoins = FormattableValue('ecoins')
		self.per = FormattableValue('per', big=True)
		self.register = 0
		self.Fregister = 0
		self.corn = FormattableValue('corn')
		self.status = 0
		self.Fstatus = ''
		self.yen = FormattableValue('yen', big=True)
		self.issued = FormattableValue('issued')
		self.game_id = 0
		self.perlimit = FormattableValue('perlimit', big=True)
		self.biores = FormattableValue('biores', 'mine')
		
		self.mine = Mine()
		self.property = Property()
		self.ferma = Ferma()
		self.business = Business()
		self.garden = Garden()
		self.generator = Generator()
		self.quarry = Quarry()
		self.tree = Tree()
		self.clan = Clan()

	async def update(self):
		if self.message:
			self.user_id = self.message.from_user.id
			self.id = self.message.from_user.id
		elif self.call:
			self.user_id = self.call.from_user.id
			self.id = self.call.from_user.id
		elif self.not_class:
			self.user_id = self.not_class
			self.id = self.not_class
		else:
			raise ValueError("Нет данных для создания класса: отсутствуют 'message' или 'call'")
		
		data, mine, property, ferma, business, garden, generator, quarry, tree, clan, rank = await db.get_user_info(self.id)
		
		self.name = data[1]
		self.balance.set(data[2], self.user_id)
		self.btc.set(data[3], self.user_id)
		self.bank.set(data[4], self.user_id)
		self.depozit.set(data[5], self.user_id)
		self.depozit_time = data[6]
		self.expe.set(data[7], self.user_id)
		self.energy.set(data[8], self.user_id)
		
		self.case[1].set(data[9], self.user_id)
		self.case[2].set(data[10], self.user_id)
		self.case[3].set(data[11], self.user_id)
		self.case[4].set(data[12], self.user_id)
		
		self.rating.set(data[13], self.user_id)
		self.games.set(data[14], self.user_id)
		self.bcoins.set(data[15], self.user_id)
		self.per.set(data[16], self.user_id)
		self.register = data[17]
		self.corn.set(data[18], self.user_id)
		self.status = data[19]
		self.issued.set(data[20], self.user_id)
		self.game_id = data[21]
		self.yen.set(data[22], self.user_id)
		self.perlimit.set(data[23], self.user_id)
		self.biores.set(mine[13], self.user_id)
		
		self.mine.update_data(mine)
		self.property.update_data(property)
		
		if ferma:
			self.ferma.update_data(ferma)
		else:
			self.ferma = None
			
		if business:
			self.business.update_data(business)
		else:
			self.business = None
			
		if garden:
			self.garden.update_data(garden)
		else:
			self.garden = None
			
		if generator:
			self.generator.update_data(generator)
		else:
			self.generator = None
			
		if quarry:
			self.quarry.update_data(quarry)
		else:
			self.quarry = None
			
		if tree:
			self.tree.update_data(tree)
		else:
			self.tree = None
			
		if clan:
			self.clan.update_data(clan, rank)
		else:
			self.clan = None
		
		self.Fstatus = get_text_status(self.status)
		self.Fregister = datetime.fromtimestamp(data[17]).strftime('%Y-%m-%d в %H:%M:%S')
		self.url = f'<a href="tg://user?id={self.user_id}">{self.name}</a>'
