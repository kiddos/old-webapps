# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from hashlib import sha256
from time import time

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import User, Paper
from .forms import PaperForm


def index(request):
  if request.session and request.session['login']:
    return redirect('user')
  else:
    return render(request, 'index.html', {'login': False})


def register(request):
  if request.method == 'POST':
    user = User.objects.create(username=request.POST['username'],
      password_sha256=sha256(request.POST['password']).hexdigest(),
      first_name=request.POST['firstname'],
      last_name=request.POST['lastname'])
    user.save()
    return redirect('login')
  else:
    return render(request, 'register.html', {'login': False})


def login(request):
  if request.method == 'POST':
    try:
      user = User.objects.get(username=request.POST['username'],
        password_sha256=sha256(request.POST['password']).hexdigest())
    except (KeyError, User.DoesNotExist):
      # Redisplay the question voting form.
      return render(request, 'login.html', {'fail': True, 'login': False})
    if user:
      request.session['login'] = True
      request.session['user_id'] = user.id
      request.session['username'] = user.username
      return redirect('user')
    else:
      return render(request, 'login.html', {'fail': True, 'login': False})
  else:
    return render(request, 'login.html', {'login': False})


def logout(request):
  request.session['login'] = False
  return redirect('login')


def user(request):
  if request.session['login']:
    papers = Paper.objects.filter(user_id=request.session['user_id'])
    return render(request, 'user.html', {
      'papers': papers,
      'login': True,
      'username': request.session['username']
    })
  else:
    return redirect('index')


def upload_file(request):
  if request.session['login']:
    if request.method == 'POST':
      form = PaperForm(request.POST, request.FILES)
      if form.is_valid():
        form.instance.user_id = request.session['user_id']
        form.save()
        return redirect('user')
    else:
      form = PaperForm()
    return render(request, 'upload.html', {
      'form': form,
      'login': True,
      'username': request.session['username']
    })
  else:
    return redirect('index')


def edit_paper(request, paper_id=0):
  if request.session['login']:
    if request.method == 'POST':
      p = Paper.objects.get(id=paper_id)
      p.title = request.POST['title']
      p.notes = request.POST['notes']
      p.save()
      return redirect('user')
    else:
      p = Paper.objects.get(id=paper_id)
      return render(request, 'edit_paper.html', {
        'login': True,
        'paper': p,
      })
  else:
    return redirect('index')
