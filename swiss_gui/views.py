from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from swiss_gui.db_controller import fetch_from_initialplayerlist;

# Create your views here.

def index(request):
    template = loader.get_template('swiss_gui/index.html')
    context = {}
    return HttpResponse(template.render(context,request))

def create_tournament(request):
    template = loader.get_template('swiss_gui/create_tournament.html')
    context = fetch_from_initialplayerlist()
    print(context)
    return HttpResponse(template.render(context,request))