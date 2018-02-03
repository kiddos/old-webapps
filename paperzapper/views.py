# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from hashlib import sha256
from time import time
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import User, Paper
from .forms import PaperForm


def check_login(request):
  try:
    if request.session['login']:
      return True
    else: return False
  except:
    return False


def index(request):
  if check_login(request):
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
      return render(request, 'login.html', {
        'fail': True,
        'login': False,
        'fail_message': 'Invalid login',
      })
    if user:
      request.session['login'] = True
      request.session['user_id'] = user.id
      request.session['username'] = user.username
      return redirect('user')
    else:
      return render(request, 'login.html', {
        'fail': True,
        'login': False,
        'fail_message': 'Invalid login',
      })
  else:
    return render(request, 'login.html', {'login': False})


def logout(request):
  request.session['login'] = False
  return redirect('login')


def user(request):
  if check_login(request):
    papers = Paper.objects.filter(user_id=request.session['user_id'])
    return render(request, 'user.html', {
      'papers': papers,
      'login': True,
      'username': request.session['username']
    })
  else:
    return redirect('index')


def save_content(paper):
  with open(paper.document.url, 'rb') as f:
    content = f.read()
    paper.document_content = content
    paper.save()


def upload_file(request):
  if check_login(request):
    if request.method == 'POST':
      form = PaperForm(request.POST, request.FILES)
      if form.is_valid():
        form.instance.user_id = request.session['user_id']
        form.save()

        save_content(form.instance)
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
  if check_login(request):
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


def retrieve_content(paper):
  if not os.path.isfile(paper.document.url):
    with open(paper.document.url, 'wb') as f:
      f.write(paper.document_content)


def download_paper(request, paper_id=0):
  if check_login(request):
    p = Paper.objects.get(id=paper_id)
    retrieve_content(p)
    return redirect('/static/' + p.get_static_download_path())
  else:
    return redirect('index')
