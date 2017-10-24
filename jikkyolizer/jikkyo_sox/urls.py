from django.conf.urls import url
from . import views
from . import login

urlpatterns = [
	url(r'^voice/$', views.Index.as_view(), name='index'),
	url(r'^new_voice/$', views.NewVoice.as_view(), name='backend'),
	url(r'^login/$', login.inpage, name="user_login"),
	url(r'^logout/$', login.outpage, name="user_logout"),
]
