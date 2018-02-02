# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from hashlib import sha256
from django.test import TestCase, Client

from .models import User


class UserTest(TestCase):
  def setUp(self):
    self.c = Client()

    self.temp_user = User.objects.create(username='John',
      password_sha256=sha256('123').hexdigest(),
      first_name='John', last_name='Doe')
    self.temp_user.save()

  def __del__(self):
    self.temp_user.delete()

  def test_create_user(self):
    self.c.post('/register/', {
      'username': 'John',
      'password': '123',
      'firstname': 'John',
      'lastname': 'Doh',
    })
    new_user = User.objects.get(username='John', first_name='John',
      last_name='Doh')
    self.assertEqual(new_user.password_sha256, sha256('123').hexdigest())
    new_user.delete()

  def test_invalid_login(self):
    response = self.c.post('/login/', {
      'username': 'John',
      'password': '0',
    })
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Invalid login')

  def test_login(self):
    response = self.c.post('/login/', {
      'username': 'John',
      'password': '123',
    })
    self.assertRedirects(response, '/paperzapper/user/')
    self.assertNotContains(response, 'Invalid login', 302)

  def test_logout(self):
    response = self.c.post('/login/', {
      'username': 'John',
      'password': '123',
    })
    self.assertRedirects(response, '/paperzapper/user/')
    self.assertNotContains(response, 'Invalid login', 302)

    response = self.c.post('/user/logout/')
    self.assertRedirects(response, '/paperzapper/login/')
