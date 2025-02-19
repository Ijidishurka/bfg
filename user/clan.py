class Clan:
	def __init__(self):
		self.id = int()
		self.balance = '0'
		self.name = ''
		self.settings = {'inv': 0, 'kick': 0, 'ranks': 0, 'kazna': 0, 'robbery': 0, 'war': 0, 'upd_name': 0}
		self.type = 0
		self.shield = 0
		self.ratting = '0'
		self.wins = 0
		self.loses = 0
		self.rank = 0
	
	def update_data(self, data, rank):
		self.id = data[0]
		self.balance = data[1]
		self.name = data[2]
		self.settings = {'inv': data[3], 'kick': data[4], 'ranks': data[5], 'kazna': data[6], 'robbery': data[7], 'war': data[8], 'upd_name': data[9]}
		self.type = data[10]
		self.shield = data[11]
		self.ratting = data[12]
		self.wins = data[13]
		self.loses = data[14]
		self.rank = rank
