from django.conf import settings
import sys, os
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiss.settings")
import django
django.setup()

from swissdutch.constants import FideTitle, Colour, FloatStatus
from swiss_gui.models import InitialPlayerList,ParticipatedPlayerList,CurrentRoundPlayerList,Round,PooledResults,ResultsHistory,TournamentInfo
import re

def fetch_from_initialplayerlist():
    ret = {"player_list":[]}
    qs = InitialPlayerList.objects.all()
    for i,q in enumerate(qs):
        ret["player_list"].append([i+1,q.name,q.rating])
    
    return ret

def create_with_playerlist(player_list):
    
    #もともと入っていたプレーヤーを消す
    InitialPlayerList.objects.all().delete()
    
    for p in player_list["playerlist"]:
        p["rating"] = int(p["rating"])
        
    player_list["playerlist"] = sorted(player_list["playerlist"],key=lambda p: -p["rating"])
    
    for i,p in enumerate(player_list["playerlist"]):
        q = InitialPlayerList(
            name = player_list["playerlist"][i]["name"],
            rating = player_list["playerlist"][i]["rating"])
        q.save()
    
    return fetch_from_initialplayerlist()
    

def set_tournament_info(name, start_date, end_date, site, organizer):
    TournamentInfo.objects.all().delete()
    
    if not start_date:
        start_date=None
    if not end_date:
        end_date=None
        

    q = TournamentInfo(name=name,
                       start_date=start_date,
                       end_date=end_date,
                       site=site,
                       organizer=organizer)        
    
    q.save()


def return_pairing():
    current_pairing = CurrentRoundPlayerList.objects.all()
    
    
    ret = {"pairing_list":[],"round":Round.objects.get().round_no}
    
    if Round.objects.get().is_finished_board_order:
        #ボード順がすでに決まっている場合
        for cp in current_pairing:
            if cp.colour_hist[-1] is 1: #colour.white == 1
                
                pairing_dict = create_pairing_dict(cp)
                pairing_dict["board_number"] = CurrentRoundPlayerList.objects.filter(name=cp.name).get().board_number[-1]
                ret["pairing_list"].append(pairing_dict)
    
            elif cp.colour_hist[-1] is 0: #colour.none == 0
                pairing_dict = create_pairing_dict_bye(cp)
                pairing_dict["board_number"] = CurrentRoundPlayerList.objects.filter(name=cp.name).get().board_number[-1]
                ret["pairing_list"].append(pairing_dict)  
        
        ret["pairing_list"] = sorted(ret["pairing_list"],key=lambda x: x["board_number"])
        
        return ret
    
    else:
        #ボード順を決める必要がある場合
        for cp in current_pairing:
            if cp.colour_hist[-1] is 1: #colour.white == 1
                
                pairing_dict = create_pairing_dict(cp)
                ret["pairing_list"].append(pairing_dict)
    
            elif cp.colour_hist[-1] is 0: #colour.none == 0
                pairing_dict = create_pairing_dict_bye(cp)
                ret["pairing_list"].append(pairing_dict)
                
        ret["pairing_list"] = sort_pairing_list(ret["pairing_list"])
        
        for rpl in ret["pairing_list"]:
            white_player = CurrentRoundPlayerList.objects.all().filter(name=rpl["white_name"]).get()

            if white_player.board_number is None:
                white_player.board_number = [rpl["board_number"],]
            else:
                white_player.board_number.append(rpl["board_number"])

            #Byeの場合を考慮
            if len(CurrentRoundPlayerList.objects.all().filter(name=rpl["black_name"])) > 0:
                black_player = CurrentRoundPlayerList.objects.all().filter(name=rpl["black_name"]).get()
                if black_player.board_number is None:
                    black_player.board_number = [rpl["board_number"],]
                else:  
                    black_player.board_number.append(rpl["board_number"])
            
            white_player.save()
            black_player.save()
        
        round = Round.objects.get()
        round.is_finished_board_order = True
        round.save()
        
        return ret

def create_pairing_dict(cp):
    black_name = CurrentRoundPlayerList.objects.filter(pairing_no=cp.opponents[-1]).get().name
    #白と黒のスコアを取得する

    if len(PooledResults.objects.filter(name=cp.name)) is not 0:
        white_score = PooledResults.objects.filter(name=cp.name).get().result
    else:
        white_score = "-"
    
    if len(PooledResults.objects.filter(name=black_name)) is not 0:
        black_score = PooledResults.objects.filter(name=black_name).get().result
    else:
        black_score = "-"
    
    pairing_dict = {
        "white_no": cp.pairing_no,
        "white_name":cp.name, 
        "black_no": cp.opponents[-1],
        "black_name":black_name,
        "white_score": white_score,
        "black_score": black_score,
        }            
    return pairing_dict


def create_pairing_dict_bye(cp):
    pairing_dict = {
        "white_no": cp.pairing_no,
        "white_name":cp.name,
        "white_score": 1,
        "black_no": "-",
        "black_name":"Bye",
        "black_score": 0,
        }
    return pairing_dict

#According to FIDE Rule D.9
def sort_pairing_list(pairing_list):
    sorted_pairing_list = sorted(pairing_list, key=board_sorting_algorithm,reverse=True)
    for i, spl in enumerate(sorted_pairing_list):
        spl["board_number"] = i+1
    return sorted_pairing_list


def board_sorting_algorithm(pairing_dict):
    sorting_order = []
    player_num = CurrentRoundPlayerList.objects.all().count()
    
    if not re.match(str(pairing_dict["black_no"]),"-"):
        
        white_score = CurrentRoundPlayerList.objects.all().filter(name=pairing_dict["white_name"]).get().score
        black_score = CurrentRoundPlayerList.objects.all().filter(name=pairing_dict["black_name"]).get().score
        white_rank = CurrentRoundPlayerList.objects.all().filter(name=pairing_dict["white_name"]).get().pairing_no
        black_rank = CurrentRoundPlayerList.objects.all().filter(name=pairing_dict["black_name"]).get().pairing_no
        first_order = max(white_score, black_score)
        second_order = white_score + black_score
        third_order = player_num - min(white_rank, black_rank) + 1
        sorting_order = [first_order, second_order, third_order]
    else:
        sorting_order = [0,0,0]
    
    return sorting_order


def return_standing():
    ret = {"standing":[],"round":Round.objects.get().round_no}
    player_standing = CurrentRoundPlayerList.objects.order_by('-score','-tiebreak_score','pairing_no').all()
    for i,ps in enumerate(player_standing):
        ret["standing"].append({"ranking":i+1,"name":ps.name,"score":ps.score,"tiebreak_score":ps.tiebreak_score})
        
        player_to_register = ParticipatedPlayerList.objects.filter(name=ps.name).get()
        player_to_register.rank = i+1
        player_to_register.score = ps.score
        player_to_register.save()
        
    return ret
    
    
def return_history():
    ret = {"history":[]}
    current_round = Round.objects.all().get().round_no
    for i in range(0,current_round-1):
        round_results = []
        round = i+1
        round_histories = ResultsHistory.objects.filter(round=round)
        for rh in round_histories:
            round_results.append({
                "white_no": rh.white_no,
                "white_name": rh.white_name,
                "white_result": rh.white_result,
                "black_no": rh.black_no,
                "black_name": rh.black_name,
                "black_result": rh.black_result,
                })
        ret["history"].append(round_results)
    return ret


#巻き戻し
def close_tournament():
    round = Round.objects.all().get()

    tournament_info = TournamentInfo.objects.all().get()
    
    if not tournament_info.is_finished:
        round.round_no = round.round_no - 1
        tournament_info.is_finished = True
    round.save()
    tournament_info.save()

def check_finished():
    return TournamentInfo.objects.all().get().is_finished

def return_names():
    return {"names": list(InitialPlayerList.objects.values_list('name',flat=True))}

if __name__ == "__main__":
    return_pairing()