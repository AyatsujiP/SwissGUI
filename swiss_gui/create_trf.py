from django.conf import settings
import sys, os
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiss.settings")
import django
django.setup()

from swissdutch.constants import FideTitle, Colour, FloatStatus
from swiss_gui.models import InitialPlayerList,ParticipatedPlayerList,CurrentRoundPlayerList,Round,PooledResults,ResultsHistory,TournamentInfo

def create_tournament_report_file():
    trf_string = {"tournament_section":[],"player_section":[]}
    player_num = ParticipatedPlayerList.objects.count()
    rated_player_num = ParticipatedPlayerList.objects.filter(rating__gt=0).count()
    tournament_name = TournamentInfo.objects.get().name if not TournamentInfo.objects.get().name is None else ""
    tournament_date = TournamentInfo.objects.get().date.strftime('%Y.%m.%d') if not TournamentInfo.objects.get().date.strftime('%Y.%m.%d') is None else ""
    round_num = Round.objects.get().round_no if not Round.objects.get().round_no is None else ""
    
    
    ret = ""
    trf_string["tournament_section"].append("012 "+ tournament_name)
    trf_string["tournament_section"].append("022 ")
    trf_string["tournament_section"].append("032 ")
    trf_string["tournament_section"].append("042 "+ tournament_date)
    trf_string["tournament_section"].append("052 ")
    trf_string["tournament_section"].append("062 " + str(player_num))
    trf_string["tournament_section"].append("072 " + str(rated_player_num))
    trf_string["tournament_section"].append("082 ")
    trf_string["tournament_section"].append("092 ")
    trf_string["tournament_section"].append("102 ")
    trf_string["tournament_section"].append("112 ")
    trf_string["tournament_section"].append("122 ")
    trf_string["tournament_section"].append("132 ")
    
    #Add column ruler
    player_section_column_length = 100 + round_num * 10
    column_ruler = ""
    for i in range(0, player_section_column_length):
        column_ruler = column_ruler + (str((i+1) % 10))
        
    trf_string["tournament_section"].append(column_ruler)
    
    column_title = "DDD SSSS X TT NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN RRRR FFF IIIIIIIIIII BBBB/BB/BB PPPP RRRR"
    
    for i in range(0, round_num):
        column_title = column_title + "  %s%s%s%s %s %s" % (round_num % 10,round_num % 10,round_num % 10,round_num % 10,round_num % 10,round_num % 10)
    
    trf_string["tournament_section"].append(column_title)
    
    
    
    #Create String
    for t in trf_string["tournament_section"]:
        ret = ret + t + "\r\n"
        
    ret = ret + "\r\n\r\n"
    
    for t in trf_string["player_section"]:
        ret = ret + t + "\r\n"
        
    return ret