from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from swiss_gui.db_controller import fetch_from_initialplayerlist, create_with_playerlist, return_pairing, return_names,return_history, return_standing
from swiss_gui.swiss_engine import create_initial_players, create_pairing, report_results, update_round
import json

# Create your views here.

def index(request):
    template = loader.get_template('swiss_gui/index.html')
    context = {}
    return HttpResponse(template.render(context,request))

def index_redirect(request):
    return redirect("index")

#トーナメントを作る
def create_tournament(request):
    template = loader.get_template('swiss_gui/create_tournament.html')
    player_list = json.loads(request.POST["playerList"])
    
    context = create_with_playerlist(player_list)
    
    #print(context)
    return HttpResponse(template.render(context,request))

def register_user(request):
    template = loader.get_template('swiss_gui/register_user.html')
    context = fetch_from_initialplayerlist()
    return HttpResponse(template.render(context,request))

#プレーヤーが確定した後に、トーナメントを開始する
def start_tournament(request):
    template = loader.get_template('swiss_gui/show_pairing_page.html')
    #トーナメントを開始
    create_initial_players()
    #ペアリングを表示
    create_pairing()
    context = return_pairing()
    return HttpResponse(template.render(context,request))

#ラウンドごとのペアリングのページを表示する
def show_pairing_page(request):
    template = loader.get_template('swiss_gui/show_pairing_page.html')
    #ペアリングを表示
    context = return_pairing()
    return HttpResponse(template.render(context,request))  

#現在の順位のページを表示する
def show_standing_page(request):
    template = loader.get_template('swiss_gui/show_standing_page.html')
    #ペアリングを表示
    context = return_standing()
    return HttpResponse(template.render(context,request))  

#結果報告ページを表示する
def show_report_page(request):
    template = loader.get_template('swiss_gui/show_report_page.html')
    context = return_names()
    return HttpResponse(template.render(context,request))


#結果履歴ページを表示する
def show_history_page(request):
    template = loader.get_template('swiss_gui/show_history_page.html')
    context = return_history()
    return HttpResponse(template.render(context,request))


#結果を報告する
def submit_result(request):
    if request.method == "POST":
        #print (request.POST["whitename"],request.POST["whiteresult"],request.POST["blackname"],request.POST["blackresult"])
        template = loader.get_template('swiss_gui/submit_result.html')
        #結果を報告
        context = report_results(request.POST["whitename"],float(request.POST["whiteresult"]),
                                 request.POST["blackname"],float(request.POST["blackresult"]))
        return HttpResponse(template.render(context,request))
    

def next_round(request):
    template = loader.get_template('swiss_gui/next_round.html')
    context = update_round()
    if context["can_update"] is 1:
        create_pairing()
        
    return HttpResponse(template.render(context,request))

def end_tournament(request):
    template = loader.get_template('swiss_gui/show_standing_page.html')
    update_round()
    context = return_standing()
    context["round"] = "Finished"
    return HttpResponse(template.render(context,request))