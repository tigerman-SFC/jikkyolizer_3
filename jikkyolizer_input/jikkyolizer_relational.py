from jikkyolizer_da import JikkyolizerAccess
import pymysql

class SearchRelation():
	def __init__(self):
		self.relation_access = JikkyolizerAccess()

	def add_relation(self, group_or_item, relation_name):
		self.relation_access.dict_update('sox_jikkyolized', { group_or_item:relation_name }, { 'group_id':group_id, 'item_id':item_id })
		
	def fetch_relation(self, relation_name, group_or_item, except_group, except_item, raw_value):
		rel_flag = 'No_speciality'
		if group_or_item == 'group':
			rels = self.relation_access.dict_select('sox_jikkyolized', { 'group_relation':relation_name })
		if group_or_item == 'item':
			rels = self.relation_access.dict_select('sox_jikkyolized', { 'item_relation':relation_name })
		rel_graph = []
		smaller = 0
		for rel in rels:
			if rel['group_id'] != except_group or rel['item_id'] != except_item:
				rel_es = self.relation_access.dict_select('sox_data_last', { 'group_id':rel['group_id'], 'item_id':rel['item_id'] })
				for rel_e in rel_es:
					if rel['item_kind'] is not None:
						item_kind = rel['item_kind']
						rel_graph.append(eval(item_kind)(rel_e['raw_value']))
						e_value = eval(item_kind)(rel_e['raw_value'])
						if e_value < raw_value:
							smaller += 1

		if item_kind == 'int' or item_kind == 'float':
			max_value = max(rel_graph)
			min_value = min(rel_graph)
			if raw_value > max_value:
				rel_flag = 'rel_max'
			elif raw_value < min_value:
				rel_flag = 'rel_min'
			elif (smaller/len(rel_graph)) < 0.1:
				rel_flag = 'rel_little'
			elif (smaller/len(rel_graph)) > 0.9:
				rel_flag = 'rel_much'

		return rel_flag


