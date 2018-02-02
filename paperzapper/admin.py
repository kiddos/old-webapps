# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User
from .models import Paper


admin.site.register(User)
admin.site.register(Paper)
