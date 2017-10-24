import sys
sys.path.append('/home/jikkyolizer/jikkyolizer_input/')

from jikkyolizer_da import JikkyolizerAccess

def fetch_new_voice(past_voices):
	to_voice_data = JikkyolizerAccess()
	sql = 'select * from voice_prior order by vocalize_prior asc, insert_timestamp desc;'
	to_voice_data.cursor.execute(sql)
	voice_priority = to_voice_data.cursor.fetchall()
	for voice_pri in voice_priority:
		voice_N = {}
		if '{0:07d}'.format(voice_pri['ID']) in past_voices.values():
			pass
		else:
			for i in range(8):
				voice_N[i] = voice_pri['voice_' + str(i)]

			return voice_pri['ID'], voice_N
	
	for i in range(8):
		voice_N[i] = 0
	return 0, voice_N

