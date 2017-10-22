"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from app.auth.views import LoginView, LogoutView, CreateUserView
from app.group.views import GroupView, GroupUsersView
from app.user.views import UserView, GetUserIdView

from app.url_handlers.views import (
   handler403,
   handler404,
   handler500,
)

urlpatterns = [
    url(r'^auth/login/$', LoginView.as_view()),
    url(r'^auth/logout/$', LogoutView.as_view()),
    url(r'^auth/create/$', CreateUserView.as_view()),
    
    url(r'^group/$', GroupView.as_view()),
    url(r'^group/(?P<group_id>\d+)/$', GroupView.as_view()),
  
    url(r'^user/$', GetUserIdView.as_view()),
    url(r'^user/(?P<user_id>\d+)/$', UserView.as_view()),
    url(r'^user/(?P<user_id>\d+)/groups/$', GroupUsersView.as_view()),
]

handle403 = handler403
handle404 = handler404
handle500 = handler500
