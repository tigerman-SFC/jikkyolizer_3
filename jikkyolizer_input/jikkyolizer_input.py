import sys
#import pymysql
import time
from datetime import datetime, timedelta

from jikkyolizer_da import JikkyolizerAccess
from jikkyolizer_vocalize_changed import JikkyolizerVocalize
from jikkyolizer_relational import SearchRelation


def main(from_jikkyolizer_string):
	group_id, item_id, raw_value, row_timestamp = parse_arg(from_jikkyolizer_string)
	d_time = datetime.strptime(row_timestamp, '%Y-%m-%d %H:%M:%S')# + timedelta(minutes=21)   #この部分、ワンチャン直った？
	row_timestamp = d_time.strftime('%Y-%m-%d %H:%M:%S')
	if judge_item_kind(raw_value) == float:
		raw_value = '{0:4.4g}'.format(raw_value)
	to_jikkyolizer_data = JikkyolizerAccess()
	to_jikkyolizer_data.dict_insert('sox_data', { 'group_id':group_id, 'item_id':item_id, 'raw_value':raw_value, 'row_timestamp':row_timestamp } )
	jikkyolize_flag, rel_flag, relations = insert_jikkyolized(item_id, group_id, raw_value, row_timestamp, to_jikkyolizer_data)
	last_change = insert_last_data(item_id, group_id, raw_value, row_timestamp, to_jikkyolizer_data)
	raw_ok, last_ok, jikkyolized_ok = check_too_past(to_jikkyolizer_data)
	item_blacklist = ['longitude', 'latitude', 'url', 'address', '運行状況', '遅延時配信日時', 'image', 'URL', 'TEL','ジャンル','住所','交通手段','営業時間']
	if item_id in item_blacklist:
		return 0
	raw_value_blacklist = ['', '-']
	if raw_value == raw_value_blacklist or len(raw_value) > 200:
		return 0
	#raw_ok, last_ok, jikkyolized_ok = number_voices(to_jikkyolizer_data)
	jikkyolized = 0
	if jikkyolized_ok == 1:
		if jikkyolize_flag == 'upper_jikkyolized':
			JikkyolizerVocalize(item_id, group_id, raw_value, row_timestamp, 'upper_jikkyolized', 2, last_change, rel_flag, relations)
			jikkyolized = 1
		elif jikkyolize_flag == 'lower_jikkyolized':
			JikkyolizerVocalize(item_id, group_id, raw_value, row_timestamp, 'lower_jikkyolized', 2, last_change, rel_flag, relations)
			jikkyolized = 1
		elif jikkyolize_flag == 'max_jikkyolized':
			JikkyolizerVocalize(item_id, group_id, raw_value, row_timestamp, 'max_jikkyolized', 1, last_change, rel_flag, relations)
			jikkyolized = 1
		elif jikkyolize_flag == 'min_jikkyolized':
			JikkyolizerVocalize(item_id, group_id, raw_value, row_timestamp, 'min_jikkyolized', 1, last_change, rel_flag, relations)
			jikkyolized = 1
		elif relations == 'rel_max' or relations == 'rel_min' or relations == 'rel_little' or relations == 'rel_much':
			JikkyolizerVocalize(item_id, group_id, raw_value, row_timestamp, 'raw_data', 2, last_change, rel_flag, relations)
			return 0

	if last_ok == 1 and jikkyolized == 0 and last_change == 1:
		JikkyolizerVocalize(item_id, group_id, raw_value, row_timestamp, 'last_changed', 3, last_change, rel_flag, relations)
		jikkyolized = 1
	if raw_ok == 1 and jikkyolized == 0:
		JikkyolizerVocalize(item_id, group_id, raw_value, row_timestamp, 'raw_data', 4, last_change, rel_flag, relations)
		jikkyolized = 1


def check_too_past(fetch_past_data):
	sql = 'select * from voice_prior;'
	fetch_past_data.cursor.execute(sql)
	number_data = fetch_past_data.cursor.fetchall()
	i = 0
	for number_datum in number_data:
		
		how_ago = int(time.mktime(datetime.now().timetuple())) - int(datetime.strptime(str(number_datum['insert_timestamp']), '%Y-%m-%d %H:%M:%S').strftime('%s'))
		how_ago_minute = int(how_ago % 3600 / 60)
		if how_ago_minute >= 4:
			sql = 'delete from voice_prior where ID=' + str(number_datum['ID']) + ';'
			fetch_past_data.cursor.execute(sql)
			fetch_past_data.connector.commit()
			i -= 1

		i += 1
	raw_ok, last_ok, jikkyolized_ok = number_voices(i)
	return raw_ok, last_ok, jikkyolized_ok

def number_voices(number_data):
	#sql = 'select count(*) from voice_prior;'
	#fetch_number_data.cursor.execute(sql)
	#number_data = fetch_number_data.cursor.fetchone()
	raw_ok = 0
	last_ok = 0
	jikkyolized_ok = 0
	if number_data < 8:
		raw_ok = 1
	if number_data < 20:
		last_ok = 1
	if number_data < 40:
		jikkyolized_ok = 1

	return raw_ok, last_ok, jikkyolized_ok



def insert_last_data(item_id, group_id, raw_value, row_timestamp, to_jikkyolizer_data):
	sql = 'select * from sox_data_last where item_id=\'' + item_id + '\' and group_id=\'' + group_id + '\';'
	to_jikkyolizer_data.cursor.execute(sql)
	last_data = to_jikkyolizer_data.cursor.fetchone()
	try:
		if last_data['raw_value'] == raw_value:
			change_flag = 0
		else:
			change_flag = 1
	except:
		change_flag = 0
	sql = 'insert into sox_data_last(group_id, item_id, raw_value, row_timestamp) values(\'' + group_id + '\', \'' + item_id + '\', \'' + raw_value + '\', \'' + row_timestamp + '\') on duplicate key update raw_value=\'' + raw_value + '\', row_timestamp=\'' + row_timestamp + '\';'
	to_jikkyolizer_data.cursor.execute(sql)
	to_jikkyolizer_data.connector.commit()
	return change_flag

def parse_arg(from_jikkyolizer_string):
	fj_string = from_jikkyolizer_string
	print (fj_string + '\n', flush=True)
	group_id_start = len("group_id")
	group_id_start += 1
	item_id_start = fj_string.find(" item_id=") 
	group_id = fj_string[group_id_start:item_id_start]
	item_id_start += len(" item_id=")
	raw_value_start = fj_string.find(" raw_value=") 
	item_id = fj_string[item_id_start:raw_value_start]
	raw_value_start += len(" raw_value=")
	timing_start = fj_string.find(" timing=")
	raw_value = fj_string[raw_value_start:timing_start]
	timing_start += len(" timing=")
	timing_process_date = len("2017-07-16")
	timing = fj_string[timing_start:timing_start + timing_process_date] + " "
	timing_process_time = len("01:00:00")
	timing += fj_string[timing_start + timing_process_date + 1 : timing_start + timing_process_date + 1 + timing_process_time]
	#print (item_id + '\n')
	#print (raw_value + '\n')
	#print (timing + '\n', flush=True)
	return group_id, item_id, raw_value, timing

def insert_jikkyolized(item_id, group_id, raw_value, row_timestamp, fetch_jikkyolized_data):
	jikkyolized_flag = 'No'
	re_calc_flag = 0
	span_no = -1
	#fetch_jikkyolized_data = JikkyolizerAccess()
	sql = 'select * from sox_jikkyolized where item_id=\'' + item_id + '\' and group_id=\'' + group_id + '\';'
	print (sql, flush=True)
	fetch_jikkyolized_data.cursor.execute(sql)
	
	print ('\n')
	result = fetch_jikkyolized_data.cursor.fetchone()
	print (result, flush=True)
	print ('\n')
	if result['total_number'] == 0:
		result['item_kind'] = judge_item_kind(raw_value) 

		init_topics = []
		result['string_0'] = str(raw_value)
		if result['item_kind'] == 'int' or result['item_kind'] == 'float':
			init_topics.extend(['max_value', 'min_value'])
		for init_topic in init_topics:
			result[init_topic] = eval(result['item_kind'])(raw_value)

		init_ones = ['total_number', 'span_0']
		for init_one in init_ones:
			result[init_one] = 1

		result['others'] = 0
		for i in range (1,10):
			result['span_' + str(i)] = 0

		result['last_0'] = row_timestamp
		
	else:
		if result['item_kind'] == 'str':
			i = 0
			others_flag = 1
			for i in range(10):
				if raw_value == result['string_' + str(i)]:
					result['span_' + str(i)] += 1
					others_flag = 0
					break
				elif result['string_' + str(i)] is None:
					others_flag = 0
					result['string_' + str(i)] = raw_value
					result['span_' + str(i)] += 1
					break
			if others_flag == 1:
				result['others'] += 1
			

		elif result['item_kind'] == 'int' or result['item_kind'] == 'float':
			raw_value = eval(result['item_kind'])(raw_value)
			distance = result['max_value'] - result['min_value']
			if distance == 0:
				if raw_value == result['max_value']:
					result['span_0'] += 1
				elif raw_value < result['min_value']:
					re_calc('min', raw_value, result, fetch_jikkyolized_data)
					jikkyolized_flag = 'min_jikkyolized'
				elif raw_value > result['max_value']:
					re_calc('max', raw_value, result, fetch_jikkyolized_data)
					jikkyolized_flag = 'max_jikkyolized'

			else:
				if raw_value < result['min_value']:
					re_calc('min', raw_value, result, fetch_jikkyolized_data)
					jikkyolized_flag = 'min_jikkyolized'
				elif raw_value > result['max_value']:
					re_calc('max', raw_value, result, fetch_jikkyolized_data)
					jikkyolized_flag = 'max_jikkyolized'
				else:
					for xi in range(10):
						i = 9 - xi
						if raw_value >= float(result['string_' + str(i)]):
							result['span_' + str(i)] += 1
							result['last_' + str(i)] = row_timestamp
							span_no = i
							break
					#how_high = raw_value - result['min_value']
					#span_no = str(int(how_high * 10 / distance))
					#if span_no == 10:
					#	span_no -= 1
					#result[span_no] += 1
					if jikkyolized_flag != 'min_jikkyolized' or jikkyolized_flag != 'max_jikkyolized':
						###judge jikkyolized_flag
						all_span = 0
						for i in range(span_no + 1):
							lower_span = result['span_' + str(i)]
						for i in range(span_no, 10):
							upper_span = result['span_' + str(i)]
						lower_ratio = (lower_span - 1)/(result['total_number'] - 1)
						upper_ratio = (upper_span - 1)/(result['total_number'] - 1)
						if lower_ratio <= 0.1:
							jikkyolized_flag = 'lower_jikkyolized'
						if upper_ratio <= 0.1:
							jikkyolized_flag = 'upper_jikkyolized'
								
						###
		elif result['item_kind'] == 'str':
			pass

		result['total_number'] += 1
	
	rel_flag = 'No_relation'
	relations = 'No'

	SR = SearchRelation()
	if result['group_relation'] is not None:
		rel_flag = SR.fetch_relation(result['group_relation'], 'group', result['group_id'], result['item_id'], raw_value)
		relations = result['group_relation']
	if result['item_relation'] is not None:
		rel_flag = SR.fetch_relation(result['item_relation'], 'item', result['group_id'], result['item_id'], raw_value)
		relations = result['item_relation']

	update_dicts = result.copy()
	del update_dicts['group_id']
	del update_dicts['item_id']
	#del update_dicts['item_kind']
	where_dicts = {'group_id': '\'' + result['group_id'] + '\'','item_id':'\'' +  result['item_id'] + '\''}

	for i in range(10):
		if update_dicts['string_' + str(i)] is not None:
			update_dicts['string_' + str(i)] = '\'' + update_dicts['string_' + str(i)] + '\''
		else:
			update_dicts['string_' + str(i)] = 'null'
		if update_dicts['last_' + str(i)] is not None:
			update_dicts['last_' + str(i)] = '\'' + str(update_dicts['last_' + str(i)]) + '\''
		else:
			update_dicts['last_' + str(i)] = 'null'
	if update_dicts['max_value'] is None:
		update_dicts['max_value'] = 'null'
	if update_dicts['min_value'] is None:
		update_dicts['min_value'] = 'null'

	if update_dicts['item_relation'] is None:
		update_dicts['item_relation'] = 'null'
	else:
		update_dicts['item_relation'] = '\'' + update_dicts['item_relation'] + '\''

	if update_dicts['group_relation'] is None:
		update_dicts['group_relation'] = 'null'
	else:
		update_dicts['group_relation'] = '\'' + update_dicts['group_relation'] + '\''



	update_dicts['item_kind'] = '\'' + update_dicts['item_kind'] + '\''

	fetch_jikkyolized_data.dict_update('sox_jikkyolized', update_dicts, where_dicts)
	#fetch_jikkyolized_data.cursor.execute(sql)
	#fetch_jikkyolized_data.connector.commit()

	return jikkyolized_flag, rel_flag, relations

def re_calc(reason, raw_value, jikkyolized_data, fetch_jikkyolized_data):

	sql = 'select * from sox_data where item_id=\'' + jikkyolized_data['item_id'] + '\' and group_id=\'' + jikkyolized_data['group_id'] + '\';'
	fetch_jikkyolized_data.cursor.execute(sql)
	past_data = fetch_jikkyolized_data.cursor.fetchall()
	
	max_value = jikkyolized_data['max_value']
	min_value = jikkyolized_data['min_value']
	if reason == 'max':
		jikkyolized_data['max_value'] = raw_value
		max_value = raw_value
	elif reason == 'min':
		jikkyolized_data['min_value'] = raw_value
		min_value = raw_value

	distance = max_value - min_value
	if jikkyolized_data['item_kind'] == 'float':
		for i in range(10):
			jikkyolized_data['string_' + str(i)] = str(round(distance) * i / 10 + min_value)
			jikkyolized_data['span_' + str(i)] = 0
	elif jikkyolized_data['item_kind'] == 'int':
		for i in range(10):
			jikkyolized_data['string_' + str(i)] = str(round(distance * i / 10) + min_value)
			jikkyolized_data['span_' + str(i)] = 0

		
	for past_datum in past_data:
		for xi in range(10):
			i = 9 - xi
			if float(past_datum['raw_value']) >= float(jikkyolized_data['string_' + str(i)]):
				jikkyolized_data['span_' + str(i)] += 1
				jikkyolized_data['last_' + str(i)] = past_datum['row_timestamp']
				break

	return jikkyolized_data
	

	




def judge_item_kind(raw_value):
	try:
		dummy = float(raw_value)
	except:
		return 'str'
	try:
		dummy = int(raw_value)
		return 'int'
	except:
		return 'float'



if __name__ == '__main__':
	f = open('/var/log/jikkyolizer/input.log', 'a')
	f.write(sys.argv[1])
	f.close()
	print (sys.argv[1])
	main(sys.argv[1])
	sys.exit()
