import os
import sys
import unittest
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from jikkyolizer_analyze import JikkyolizerAnalyze

import freezegun

class test_PATH(unittest.TestCase):
	def test_path(self):
		""" 
		pathが通っているかの確認
		"""
		self.assertEqual(BASE_DIR, '/home/jikkyolizer/jikkyolizer_input')

class test_JikkyolizerAnalyze(unittest.TestCase):
	def test_calc_average_value(self):
		ja = JikkyolizerAnalyze()
		with freezegun.freeze_time('2017-09-29 03:04:05'):

		
			


