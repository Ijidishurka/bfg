from decimal import Decimal

from assets.transform import transform_int, transform
from commands import db


class FormattableValue:
	def __init__(self, column, table='users', user_id=None, big=False, value=0):
		self.value = value
		self.column = column
		self.user_id = user_id
		self.table = table
		self.big = big
	
	def get(self):
		if self.big:
			return str(self.value)
		return int(self.value)
	
	def set(self, value=0, user_id=None):
		self.value = value
		if user_id:
			self.user_id = user_id
	
	async def upd(self, summ, action='') -> None:
		summ = int(summ)
		
		if not self.user_id:
			raise ValueError("Для выполнения этой функции вам необходимо передать user_id.")
		
		if not self.big:
			if action in ['-', '+']:
				sql = f'UPDATE {self.table} SET {self.column} = {self.column} {action} ? WHERE user_id = ?'
			else:
				sql = f'UPDATE {self.table} SET {self.column} = ? WHERE user_id = ?'
			await db.sql_zapros(sql, summ, self.user_id)
		else:
			if action == '-':
				new_value = int(Decimal(self.value) - Decimal(summ))
			elif action == '+':
				new_value = int(Decimal(self.value) + Decimal(summ))
			else:
				new_value = summ
			
			self.value = new_value
			new_value = str(new_value)
			sql = f'UPDATE {self.table} SET {self.column} = ? WHERE user_id = ?'
			await db.sql_zapros(sql, new_value, self.user_id)
	
	def tr(self) -> str:
		return transform_int(self.value)
	
	def trt(self) -> str:
		return transform(self.value)
	
	def __str__(self):
		return str(self.value)
	
	def __int__(self):
		return int(self.value)
	
	def __float__(self):
		return float(self.value)
	
	def __getattr__(self, item):
		return getattr(self.value, item)
	
	def __repr__(self):
		return int(self.value)