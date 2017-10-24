from jikkyolizer_vocalize_change import MakeVoice
from jikkyolizer_da import JikkyolizerAccess
import datetime
from dateutil.relativedelta import relativedelta
import threading



class JikkyolizerAnalyze(object):
	def __init__(self, group_id = None, item_id = None):
		self.ja = JikkyolizerAccess()
		self.group_id = group_id
		self.item_id = item_id
		self.search_sessions = ['week', 'month', 'year']

	def flexible_detect_group_id(func):
		if group_id is None:
			if self.group_id is not None:
				group_id = self.group_id
				item_id = self.item_id
			else:
				raise 'group_id is not detected'
		func(self)
		return wrapper
		
	@flexible_detect_group_id
	def get_past_item_session(self, session_from, session_to, group_id = None, item_id = None):
		where_sql = 'where group_id=' + group_id + ' and item_id=' + item_id + ' row_timestamp>' + session_from + 'and row_timestamp<' + 'session_to'
		return self.ja.raw_select('sox_data', ['raw_value', 'row_timestamp'], where_sql)

	def calc_past_item_average(self, general_history):
		value_history_total = 0.0
		number_of_history = 0
		for gh in general_history:
			value_history_total += float(gh['raw_value'])
			number_of_history += 1
		return value_history_total / number_of_history 
			
	@flexible_detect_group_id
	def calc_average_value(self, group_id = None, item_id = None):
		now = datetime.datetime.now()
		search_sessions = ['week', 'month', 'year']
		search_trend = ['increase', 'decrease']
		data = {}
		for ss in self.search_sessions:
			data[ss] = {}
			for st in search_trend:
				data[ss][st] = True
			
		for i in range(4):
			for ss in search_sessions:
				data[ss][i] = { 'history' : [], 'session_from' : None, 'session_to' : None }
				data[ss][i]['session_from'] = now - relativedelta(eval(ss + 's') = i)
				data[ss][i]['session_to'] = session_from - relativedelta(eval(ss + 's') = 1)
				data[ss][i]['history'] = self.get_past_item_session(group_id, item_id, data[ss][i]['session_from'], data[ss][i]['session_to'])
				data[ss][i]['average'] = self.calc_past_item_average(data[ss][i]['history'])
			if i > 0:
				if data[ss][i]['average'] >= data[ss][i - 1]['average']:
					data[ss]['decrease'] = False
				if data[ss][i]['average'] <= data[ss][i - 1]['average']:
					data[ss]['increase'] = False

		return data


class TestThread(threading.Thread):
	def __init__(self, group_id, item_id):
		super(TestThread, self).__init__()
		self.group_id = group_id
		self.item_id = item_id
		self.ja = JikkyolizerAnalyze(self.group_id, self.item_id)
		self.ss_j = [ja.search_sessions[0]:'1ヶ月', ja.search_sessions[1]:'半年', ja.search_sessions[2]:'5年', ja.search_sessions[3]:'10年']

	def run(self):
		result = ja.calc_average_value()
		is_vocalized = False
		for ss in ja.search_sessions:
			sentence = 'これを分析したところ、'
			if result[ss]['increase']:
				sentence += self.ss_j[ss] + 'の間に'
				sentence += '値が増加傾向にあることがわかりました。'
				MakeVoice.raw_vocalize('')
				is_vocalized = True
			if result[ss]['decrease']:
				sentence += self.ss_j[ss] + 'の間に'
				sentence += '値が減少傾向にあることがわかりました。'
				MakeVoice.raw_vocalize('')
				is_vocalized = True

		if is_vocalized:
			MakeVoice.raw_vocalize(sentence, '')
		





		
		
