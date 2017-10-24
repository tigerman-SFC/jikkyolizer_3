from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.http import HttpResponse as AjaxResponse
from . import tools

# Create your views here.

class Index(LoginRequiredMixin,TemplateView):
	template_name = 'voice.html'
	def get(self, request):
		context = {
			'voice_id' : 0
		}
		return render(
			request,
			'voice.html',
			context
		)
		
			


class NewVoice(LoginRequiredMixin, TemplateView):
	def post(self, request):
		#new_voice_no = tools.
		#new_voice_no = '00001' 
		test='A'
		past_voices = {}
		for i in range(40):
			past_voices[i] = (request.POST['used_voice' + str(i)])
		new_voice, voice_N = tools.fetch_new_voice(past_voices)
		new_voice7 = ''
		for i in range(8):
			if voice_N[i] == 1:
				new_voice7 += '{0:07d}'.format(new_voice) + '-' + str(i)
				new_voice7 += ';'

		new_voice7 += '{0:07d}'.format(new_voice) + ';';
		return AjaxResponse(new_voice7)

	def get(self, request):
		tools.fetch_new_voice({1:'1'})
		return AjaxResponse('a')



