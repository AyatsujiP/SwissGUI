from django.conf import settings
import sys, os
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiss.settings")
import django
django.setup()

from swiss_gui.models import  InitialPlayerList,ParticipatedPlayerList,CurrentRoundPlayerList,Round,PooledResults

def fetch_from_initialplayerlist():
    ret = {"player_list":[]}
    qs = InitialPlayerList.objects.all()
    for i,q in enumerate(qs):
        ret["player_list"].append([q.id,q.name,q.rating])
    
    return ret

if __name__ == "__main__":
    ret = fetch_from_initialplayerlist()