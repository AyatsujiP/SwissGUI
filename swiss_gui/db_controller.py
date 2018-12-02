from django.conf import settings
import sys, os
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiss.settings")
import django
django.setup()

from swissdutch.constants import FideTitle, Colour, FloatStatus
from swiss_gui.models import  InitialPlayerList,ParticipatedPlayerList,CurrentRoundPlayerList,Round,PooledResults,ResultsHistory


def fetch_from_initialplayerlist():
    ret = {"player_list":[]}
    qs = InitialPlayerList.objects.all()
    for i,q in enumerate(qs):
        ret["player_list"].append([q.id,q.name,q.rating])
    
    return ret


def return_pairing():
    current_pairing = CurrentRoundPlayerList.objects.all()
    
    ret = {"pairing_list":[],"round":Round.objects.get().round_no}
    
    for cp in current_pairing:
        if cp.colour_hist[-1] is 1: #colour.white == 1
            
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
            ret["pairing_list"].append(pairing_dict) 
            
        elif cp.colour_hist[-1] is 0: #colour.none == 0
            pairing_dict = {
                "white_no": cp.pairing_no,
                "white_name":cp.name,
                "white_score": 1,
                "black_no": "-",
                "black_name":"Bye",
                "black_score": 0
                }
            ret["pairing_list"].append(pairing_dict)        

    return (ret)


def return_standing():
    ret = {"standing":[]}
    player_standing = CurrentRoundPlayerList.objects.order_by('-score','-tiebreak_score','pairing_no').all()
    for i,ps in enumerate(player_standing):
        ret["standing"].append({"ranking":i+1,"name":ps.name,"score":ps.score,"tiebreak_score":ps.tiebreak_score})
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


def return_names():
    return {"names": list(InitialPlayerList.objects.values_list('name',flat=True))}

if __name__ == "__main__":
    return_pairing()