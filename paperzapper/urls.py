from django.conf.urls import url

import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^register/', views.register, name='register'),
  url(r'^login/', views.login, name='login'),
  url(r'^user/$', views.user, name='user'),
  url(r'^user/upload', views.upload_file, name='uploads'),
  url(r'^user/logout', views.logout, name='logout'),
  url(r'^user/paper/(?P<paper_id>\d+)', views.edit_paper, name='edit_paper'),
]
