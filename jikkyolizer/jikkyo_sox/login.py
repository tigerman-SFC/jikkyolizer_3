# -*- coding: utf-8 -*-
#http://blog.hitsuji.me/use-template-files/からのコピペを元に改変。
#ただ、他のページでも同じような処理をしてあったので、これを使った。
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django import forms
from django.contrib.auth import authenticate, login, logout

def inpage(request):
    attention = ''
    
    if request.POST:
        form = Login_form(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.GET.get('next') is not None:
                        # next=の後のurlへ飛ぶ
                        return redirect(request.GET['next'])
                    else:
                        # topページへ飛ぶ
                        return redirect('jikkyo_sox:index')
        if not authenticate(username=username, password=password):
            attention = 'Wrong user name or passwsord'
                        
    # New form when not the request is get.
    else:
        if request.user.is_authenticated:
            return redirect('jikkyo_sox:index')
        form = Login_form()
    return render(request, 'login.html', {'form' : form, 'attention' : attention})



class Login_form(forms.Form):
    username = forms.CharField(label="User name")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    #パスワードが間違っていた時の処理
    def clean(self):
        cleaned_data = super(Login_form, self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not authenticate(username=username, password=password):
            #raise forms.ValidationError("Wrong user name or passwsord")
            pass
        return self.cleaned_data


def outpage(request):
    form = Login_form()
    logout(request)
    return redirect('jikkyo_sox:user_login')
