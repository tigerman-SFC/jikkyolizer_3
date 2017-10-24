import pymysql

class JikkyolizerAccess(object):
	def __init__(self):
		self.get_cursor_database_access()
		#self.connector = self.fetch_object['connector']
		#self.cursor = self.fetch_object['cursor']

	def get_cursor_database_access(self):
		self.connector = pymysql.connect(host="172.17.0.3", db="jikkyolizer_data", user="root", passwd="sqladmin", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.connector.cursor()
		#self.access_object = { 'connector' : self.connector, 'cursor' : self.connector.cursor()}
		#return access_object

	def dict_insert(self, Table, Dicts):
		Params = Dicts.keys()
		Values = Dicts.values()
		SetParams = ''
		SetValues = ''
		StringValue = ''
		for Param in Params:
			if SetParams != '': 
				SetParams += ','
			SetParams += Param
		for Value in Values:
			if SetValues != '':
				SetValues += ','
			if isinstance(Value, str):
				SetValues += "'" + str(Value) + "'"
			else:
				SetValues += str(Value)
		sql = "insert into " + str(Table) + " (" + SetParams + ") values(" + SetValues + ");"
		#print (sql)
		self.cursor.execute(sql)
		self.connector.commit()
		return 0 

	def dict_update(self, Table, update_dicts, where_dicts):
		Params = update_dicts.keys()
		Values = update_dicts.values()
		update_string = 'update ' + Table + ' set '
		for Param,Value in zip(Params, Values):
			#if isinstance(Value, str):
			#	update_string += Param + '=\'' + str(Value) + '\','
			#else:
			update_string += Param + '=' + str(Value) + ','

		update_string = update_string[:-1]
		update_string += ' where '
		where_params = where_dicts.keys()
		where_values = where_dicts.values()
		for where_param, where_value in zip(where_params, where_values):
			#if isinstance(where_value, str):
			#	update_string += where_param + '=\'' + str(where_value) + '\' and '
			#else:
			update_string += where_param + '=' + str(where_value) + ' and '
		update_string = update_string[:-5]

		print(update_string, flush=True)

		self.cursor.execute(update_string)
		self.connector.commit()
		return 0
			
	def dict_select(self, table, where_dicts):
		Params = where_dicts.keys()
		Values = where_dicts.values()
		sql = 'select * from ' + table + ' where '
		i = 0
		for param,value in zip(Params, Values):
			if i == 1:
				sql += ' and '
			if isinstance(value, str):
				sql += param + '=\'' + value + '\''
			else:
				sql += param + '=' + value
			i = 1
		print(sql, flush=True)
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def from_list_to_str(self, from_list):
		to_str = ''
		for from_item in from_list:
			to_str += from_item + ','
		to_str = to_str[:-1]
		return to_str
			
	def raw_select(self, table, target_list = ['*'], where_str = None):
		sql = 'select ' + self.from_list_to_str(target_list) + ' from ' + table
		if where_str is not None:
			sql += ' ' + where_str
		sql += ';'
		self.cursor.execute(sql)
		return self.cursor.fetchall()
		





