"""swiss URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from swiss_gui import views

urlpatterns = [
    url('accounts/',include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index_redirect,name='index_redirect'),
    url(r'swiss_gui/$', views.index,name='index'),
    url(r'swiss_gui/register_user/', views.register_user,name='register_user'),
    url(r'swiss_gui/register_error/', views.register_error,name='register_error'),
    url(r'swiss_gui/create_tournament/', views.create_tournament,name='create_tournament'),
    url(r'swiss_gui/start_tournament/', views.start_tournament,name='start_tournament'),
    url(r'swiss_gui/show_pairing_page/', views.show_pairing_page,name='show_pairing_page'),
    url(r'swiss_gui/show_standing_page/', views.show_standing_page,name='show_standing_page'),
    url(r'swiss_gui/show_report_page/', views.show_report_page,name='show_report_page'),
    url(r'swiss_gui/show_history_page/', views.show_history_page,name='show_history_page'),
    url(r'swiss_gui/submit_result/', views.submit_result,name='submit_result'),
    url(r'swiss_gui/next_round/', views.next_round,name='next_round'),
    url(r'swiss_gui/download_trf/tournament_report_file.txt', views.douwnload_trf,name='download_trf'),
    url(r'swiss_gui/end_tournament/', views.end_tournament,name='end_tournament'),
    
]
