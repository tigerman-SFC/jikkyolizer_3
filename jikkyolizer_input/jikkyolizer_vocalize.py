from jikkyolizer_da import JikkyolizerAccess
import time
from datetime import datetime
import subprocess

class JikkyolizerVocalize():
	def __init__(self, item_id, group_id, raw_value, row_timestamp, reason, vocalize_prior, is_change, rel_flag, relations):
		to_vocalize_data = JikkyolizerAccess()
		sql = 'SELECT auto_increment FROM information_schema.tables WHERE table_name = "voice_prior";'
		to_vocalize_data.cursor.execute(sql)
		jikkyo_id_pre = to_vocalize_data.cursor.fetchone() 
		jikkyo_id = jikkyo_id_pre['auto_increment']
		voice_prior_dicts = { 'vocalize_kind':reason, 'vocalize_prior':vocalize_prior, 'group_id':group_id, 'item_id':item_id, 'raw_value':raw_value, 'row_timestamp':row_timestamp, 'relation_reason':rel_flag, 'voice_0':1, 'voice_1':1, 'voice_2':1, 'voice_3':1, 'voice_4':1, 'voice_5':0, 'voice_6':0, 'voice_7':0 }
		if reason == 'raw_data' and reason == 'last_changed':
			pass
		elif reason == 'upper_jikkyolized' or reason == 'lower_jikkyolized' or reason == 'max_jikkyolized' or reason == 'min_jikkyolized' :
			voice_prior_dicts['voice_5'] = 1

		if rel_flag != 'No_relation' and rel_flag != 'No_speciality':
			voice_prior_dicts['voice_6'] = 1
			voice_prior_dicts['voice_7'] = 1

		to_vocalize_data.dict_insert('voice_prior', voice_prior_dicts)
		voice_prior_dicts['ID'] = jikkyo_id
		to_vocalize_data.dict_insert('voice_prior_record', voice_prior_dicts)
		jikkyo_id7 = '{0:07d}'.format(jikkyo_id)
		
		how_ago = int(time.mktime(datetime.now().timetuple())) - int(datetime.strptime(row_timestamp, '%Y-%m-%d %H:%M:%S').strftime('%s'))
		how_ago_second = how_ago % 60
		how_ago_minute = int(how_ago % 3600 / 60)
		how_ago_hour = int(how_ago % 86400 / 3600)
		vocalize_sentence = '今から' 
		if how_ago_minute < 1:
			vocalize_sentence += str(how_ago_second) + '秒まえ、'
		elif how_ago_minute >= 1 and how_ago_hour < 1:
			vocalize_sentence += str(how_ago_minute) + '分まえ、'
		else:
			vocalize_sentence += str(how_ago_hour) + '時間まえ、'
		
		cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + vocalize_sentence + '\'" -d "speaker=hikari" -d "speed=100" -o /var/www/html/voices/jikkyo-' + jikkyo_id7 +'-0.wav'
		subprocess.call(cmd, shell=True) 

		vocalize_sentence = group_id + 'の' + item_id  
		
		
		cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + vocalize_sentence + '\'" -d "speaker=hikari" -d "speed=100" -d "pitch=100" -d "volume=100" -o /var/www/html/voices/jikkyo-' + jikkyo_id7 +'-1.wav'
		subprocess.call(cmd, shell=True) 
		
		vocalize_sentence = 'の値が'
		cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + vocalize_sentence + '\'" -d "speaker=hikari" -d "speed=100" -o /var/www/html/voices/jikkyo-' + jikkyo_id7 +'-2.wav'
		subprocess.call(cmd, shell=True) 
		
		vocalize_sentence = str(raw_value)
		cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + vocalize_sentence + '\'" -d "speaker=hikari" -d "speed=100" -o /var/www/html/voices/jikkyo-' + jikkyo_id7 +'-3.wav'
		subprocess.call(cmd, shell=True) 

		if is_change == 1:
			vocalize_sentence = 'になりました。'
		else:
			vocalize_sentence = 'を示しました。'
		cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + vocalize_sentence + '\'" -d "speaker=hikari" -d "speed=100" -o /var/www/html/voices/jikkyo-' + jikkyo_id7 +'-4.wav'
		subprocess.call(cmd, shell=True) 

		if reason == 'upper_jikkyolized':
			vocalize_sentence = 'これはとても高い値です。'
			cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + vocalize_sentence + '\'" -d "speaker=hikari" -d "speed=100" -d "pitch=100" -d "volume=100" -o /var/www/html/voices/jikkyo-' + jikkyo_id7 +'-5.wav'
			subprocess.call(cmd, shell=True) 
		elif reason == 'lower_jikkyolized':
			vocalize_sentence = 'これはとても低い値です。'
			cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + vocalize_sentence + '\'" -d "speaker=hikari" -d "speed=100" -d "pitch=100" -d "volume=100" -o /var/www/html/voices/jikkyo-' + jikkyo_id7 +'-5.wav'
			subprocess.call(cmd, shell=True) 
		elif reason == 'max_jikkyolized':
			vocalize_sentence = 'これは今までで最高の値です。'
			cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + vocalize_sentence + '\'" -d "speaker=hikari" -d "speed=100" -d "pitch=100" -d "volume=100" -o /var/www/html/voices/jikkyo-' + jikkyo_id7 +'-5.wav'
			subprocess.call(cmd, shell=True) 
		elif reason == 'min_jikkyolized':
			vocalize_sentence = 'これは今までで最低の値です。'
			cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + vocalize_sentence + '\'" -d "speaker=hikari" -d "speed=100" -d "pitch=100" -d "volume=100" -o /var/www/html/voices/jikkyo-' + jikkyo_id7 +'-5.wav'
			subprocess.call(cmd, shell=True) 
		
		if rel_flag != 'No_relation' and rel_flag != 'No_speciality':
			vocalize_sentence = 'なお、同種類の' + relations + 'の値の中で'
			cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + vocalize_sentence + '\'" -d "speaker=hikari" -d "speed=100" -o /var/www/html/voices/jikkyo-' + jikkyo_id7 +'-6.wav'
			subprocess.call(cmd, shell=True) 
			if rel_flag == 'rel_max':
				vocalize_sentence = '最高の値を示しています。'
				cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + vocalize_sentence + '\'" -d "speaker=hikari" -d "speed=100" -d "pitch=100" -d "volume=100" -o /var/www/html/voices/jikkyo-' + jikkyo_id7 +'-7.wav'
				subprocess.call(cmd, shell=True) 
			if rel_flag == 'rel_min':
				vocalize_sentence = '最低の値を示しています。'
				cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + vocalize_sentence + '\'" -d "speaker=hikari" -d "speed=100" -d "pitch=100" -d "volume=100" -o /var/www/html/voices/jikkyo-' + jikkyo_id7 +'-7.wav'
				subprocess.call(cmd, shell=True) 
			if rel_flag == 'rel_much':
				vocalize_sentence = 'とても高い値を示しています。'
				cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + vocalize_sentence + '\'" -d "speaker=hikari" -d "speed=100" -d "pitch=100" -d "volume=100" -o /var/www/html/voices/jikkyo-' + jikkyo_id7 +'-7.wav'
				subprocess.call(cmd, shell=True) 
			if rel_flag == 'rel_little':
				vocalize_sentence = 'とても低い値を示しています。'
				cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + vocalize_sentence + '\'" -d "speaker=hikari" -d "speed=100" -d "pitch=100" -d "volume=100" -o /var/www/html/voices/jikkyo-' + jikkyo_id7 +'-7.wav'
				subprocess.call(cmd, shell=True) 
		
def raw_vocalize(sentence, jikkyo_id, speaker, speed=100, pitch=100, volume=100):
	cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + str(sentence) + '\'" -d "speaker=' + str(speaker) + '" -d "speed=' + str(speed) + '" -d "pitch=' + str(pitch) + '" -d "volume=' + str(volume) + '" -o /var/www/html/voices/jikkyo-' + str(jikkyo_id) +'-5.wav'
	subprocess.call(cmd, shell=True) 

class MakeVoice():
	@classmethod
	def raw_vocalize(cls, sentence, kind, content_ID, speaker, speed=100, pitch=100, volume=100):
		cmd = 'curl "https://api.voicetext.jp/v1/tts" -u "mpbw1hnrp32pdde7:" -d "text= \'' + str(sentence) + '\'" -d "speaker=' + str(speaker) + '" -d "speed=' + str(speed) + '" -d "pitch=' + str(pitch) + '" -d "volume=' + str(volume) + '" -o /var/www/html/voices/' + kind + '/' + content_ID +'.wav'
		subprocess.call(cmd, shell=True)



