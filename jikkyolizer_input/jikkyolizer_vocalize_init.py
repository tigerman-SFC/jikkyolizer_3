import sys
from jikkyolizer_vocalize_changed import MakeVoice


SPEAKER = 'show'
class MakeInitialVoices():
	@classmethod
	def make_before_time(cls):
		for i in range(1, 60):
			sentence = '今から' + str(i) + '秒前、'
			content_ID = 's_' + str(i)
			speaker = 'show'
			MakeVoice.raw_vocalize(sentence, 'before_time', content_ID, SPEAKER, speed = 110)
			sentence = '今から' + str(i) + '分前、'
			content_ID = 'm_' + str(i)
			MakeVoice.raw_vocalize(sentence, 'before_time', content_ID, SPEAKER, speed = 110)

	@classmethod
	def make_is_changed(cls):
		MakeVoice.raw_vocalize('になりました。', 'is_changed', 'changed', SPEAKER, speed = 110)
		MakeVoice.raw_vocalize('を示しました。', 'is_changed', 'unchanged', SPEAKER, speed = 110)
		MakeVoice.raw_vocalize('になっていました。', 'is_changed', 'past-changed', SPEAKER, speed = 110)
		MakeVoice.raw_vocalize('を示していました。', 'is_changed', 'past-unchanged', SPEAKER, speed = 110)

	@classmethod
	def make_others(cls):
		MakeVoice.raw_vocalize('今回の', 'make_others', 'konkaino', SPEAKER, speed = 110)
		MakeVoice.raw_vocalize('の値が', 'make_others', 'no_ataiga', SPEAKER, speed = 110)
		MakeVoice.raw_vocalize('の値は', 'make_others', 'no_ataiha', SPEAKER, speed = 90)

	@classmethod
	def make_jikkyolized_result(cls):
		MakeVoice.raw_vocalize('の値はとても低い値です。', 'jikkyolized_result', 'lower', SPEAKER, speed = 80, pitch = 75, volume = 150)
		MakeVoice.raw_vocalize('の値はとても高い値です。', 'jikkyolized_result', 'upper', SPEAKER, speed = 80, pitch = 150, volume = 150)
		MakeVoice.raw_vocalize('の値は今までで最低の値です。', 'jikkyolized_result', 'lowest', SPEAKER, speed = 80, pitch = 200, volume = 150)
		MakeVoice.raw_vocalize('の値は今までで最高の値です', 'jikkyolized_result', 'uppermost', SPEAKER, speed = 80, pitch = 50, volume = 150)

	@classmethod
	def make_analyzed_result(cls):
		for session_id, session in {'week':'1週間', 'month':'1ヶ月間', 'year':'1年間'}.items():
			MakeVoice.raw_vocalize('はこの'+session+'減少傾向にあります。', 'analyzed_result', session_id+'-decrease', SPEAKER, speed = 80, pitch = 75, volume = 170)
			MakeVoice.raw_vocalize('はこの'+session+'増加傾向にあります。', 'analyzed_result', session_id+'-increase', SPEAKER, speed = 80, pitch = 150, volume = 170)

def main():
	#MakeInitialVoices.make_before_time()
	MakeInitialVoices.make_is_changed()
	MakeInitialVoices.make_others()
	MakeInitialVoices.make_jikkyolized_result()
	MakeInitialVoices.make_analyzed_result()

if __name__ == '__main__':
	main()
	sys.exit()
