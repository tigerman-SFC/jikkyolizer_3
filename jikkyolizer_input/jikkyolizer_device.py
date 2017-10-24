import sys
#import pymysql
import time

from jikkyolizer_da import JikkyolizerAccess
from jikkyolizer_vocalize_changed import MakeVoice

def main(from_java_string):
	fj_string = from_java_string
	group_id_start = len('group_id=')
	group_id_start += 1
	group_id_end = fj_string.find(',')
	group_id = fj_string[group_id_start:group_id_end]
	item_id_start = fj_string.find('item_id')
	item_id_start += len('item_id')
	item_id_start += 1
	item_id_end = fj_string.find(',')
	item_id = fj_string[item_id_start:item_id_end]
	#item_id = fj_string[item_id_start:-1]
	group_name_start = fj_string.find('group_name')
	group_name_start += len('group_name')
	group_name_start += 1
	group_name = fj_string[group_name:-1]
	print (group_id + item_id +  group_name, flush=True)
	#items = []
	to_jikkyolizer_data = JikkyolizerAccess()
	#if item_id is None:  #false
	if isinstance(item_id, str):
		dummy = 'aaa'
	else:
		dummy = 'ccc'
	#if group_id is None:   #false
	if isinstance(group_id, str):
		dummy2 = 'bbb'
	else:
		dummy2 = 'ddd'

	try:
		to_jikkyolizer_data.dict_insert('sox_jikkyolized',{ 'group_id':group_id, 'item_id':item_id, 'total_number':0 })
	except:
		#f.write('group_id=' + group_id + ', item_id=' +item_id +  '\n')
		#f.flush()
		pass
	pre_ID = to_jikkyolizer_data.dict_select('sox_jikkyolized', { 'group_id':group_id, 'item_id':item_id })
	voice_ID = '{0:07d}'.format(pre_ID[0]['ID'])
	pre_ID = to_jikkyolizer_data.dict_insert('sox_id_name_relation', { 'device_id':group_id, 'device_name':item_id })
	MakeVoice.raw_vocalize(group_name+'の'+item_id, 'group_item', 'id-' + voice_ID)
	return item_id, str(type(item_id))

def ex_main():
	to_jikkyolizer_data = JikkyolizerAccess()
	to_jikkyolizer_data.dict_insert('sox_jikkyolized',{ 'group_id':'"123"', 'item_id':'ううう' })

if __name__ == '__main__':
	try:
		#time.sleep(3)
		f = open('/var/log/jikkyolizer/device.log', 'a')
		f.write(sys.argv[1] + '\n')
	except:
		ex_main()
	print (sys.argv[1])
	ret, ret_type = main(sys.argv[1])
	f.flush()
	f.close()
	f.close()
	sys.exit()
