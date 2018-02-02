# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import models


class User(models.Model):
  username = models.CharField(max_length=512)
  password_sha256 = models.CharField(max_length=512)
  first_name = models.CharField(max_length=512)
  last_name = models.CharField(max_length=512)


class Paper(models.Model):
  user = models.ForeignKey(User)
  title = models.CharField(max_length=512)
  document = models.FileField(upload_to='papers/')
  notes = models.TextField()
  upload_date = models.DateTimeField(auto_now_add=True)

  def get_static_download_path(self):
    return os.path.basename(self.document.url)
