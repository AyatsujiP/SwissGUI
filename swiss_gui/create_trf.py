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
    
    players = ParticipatedPlayerList.objects.order_by('-rating','name').all()
    
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
        
    trf_string["player_section"].append(column_ruler)
    
    column_title = "DDD SSSS X TT NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN RRRR FFF IIIIIIIIIII BBBB/BB/BB PPPP RRRR"
    
    for i in range(0, round_num):
        column_title = column_title + "  %s%s%s%s %s %s" % ((i+1) % 10,(i+1) % 10,(i+1) % 10,(i+1) % 10,(i+1) % 10,(i+1) % 10)
    
    trf_string["player_section"].append(column_title)
    
    for player in players:
        player_string = "001 "
        #startingrank number
        player_string = player_string + str(player.pairing_no).rjust(4)
        
        player_string =padding(player_string)
        
        #Gender
        player_string = player_string + " "
        
        player_string =padding(player_string)
        
        #Title
        player_string = player_string + "  "
        
        player_string =padding(player_string)
        
        #Name
        player_string = player_string + player.name.ljust(33)
        
        player_string =padding(player_string)
        
        #Rating
        player_string = player_string + str(player.rating).rjust(4)

        player_string =padding(player_string)
        
        #Federation        
        player_string = player_string + "   "

        player_string =padding(player_string)
        
        #FIDE number
        player_string = player_string + "           "

        player_string =padding(player_string)
        
        #Birthday
        player_string = player_string + "xxxx/xx/xx"
        
        player_string =padding(player_string)
        
        #Points
        player_string = player_string + ("%1.1f" % player.score).rjust(4)
        
        player_string =padding(player_string)
        
        #Points
        player_string = player_string + ("%s" % player.rank).rjust(4)
        
        player_string =padding(player_string)
                        
        trf_string["player_section"].append(player_string)
    
    
    
    #Create String
    for t in trf_string["tournament_section"]:
        ret = ret + t + "\r\n"
        
    ret = ret + "\r\n"
    
    for t in trf_string["player_section"]:
        ret = ret + t + "\r\n"
        
    return ret


def padding(player_string):
    return player_string + " "