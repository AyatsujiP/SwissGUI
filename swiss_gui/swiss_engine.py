from django.conf import settings
import sys, os
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiss.settings")
import django
django.setup()

from swissdutch.dutch import DutchPairingEngine
from swissdutch.constants import FideTitle, Colour, FloatStatus
from swissdutch.player import Player

import csv
import copy
import sys
from swiss_gui.models import  InitialPlayerList,ParticipatedPlayerList,CurrentRoundPlayerList,Round,PooledResults


def create_initial_players():
    #プレーヤーリストを、swiss_gui_participatedplayerlistテーブルに登録する。
    players = InitialPlayerList.objects.order_by('rating').reverse().all()
    
    #もともと入っていたレコードを消す
    ParticipatedPlayerList.objects.all().delete()
    CurrentRoundPlayerList.objects.all().delete()
    Round.objects.all().delete()
    
    #swiss_gui_initialplayerlistテーブルから追加する。
    for i, player in enumerate(players):
        q = ParticipatedPlayerList(
            name = player.name,
            rating = player.rating,
            pairing_no = i+1,
            score = 0,
            float_status = 0
            )
        q.save()
        q = CurrentRoundPlayerList(
            name = player.name,
            rating = player.rating,
            pairing_no = i+1,
            score = 0,
            float_status = 0
            )
        q.save()
    
    q = Round(round_no = 1)
    q.save()
    
    return


def show_pairing():
    engine = DutchPairingEngine()
    #現在のラウンド数を取得する
    round_no = Round.objects.get().round_no
    
    #タプルに変換するためのリスト
    player_class_list = []
    #検索用
    player_class_dict = {}
    
    #playerクラスを作る
    players = CurrentRoundPlayerList.objects.order_by('pairing_no').all()
    for p in players:
        if round_no is 1:
            distinct_player = Player(name=p.name,
                                 rating=p.rating,
                                 pairing_no = p.pairing_no,
                                 score=p.score,
                                 float_status=p.float_status)
            player_class_list.append(distinct_player)
            player_class_dict[p.pairing_no] = p.name
        else:
            distinct_player = Player(name=p.name,
                                 rating=p.rating,
                                 pairing_no = p.pairing_no,
                                 score=p.score,
                                 float_status=p.float_status,
                                 opponents=tuple(p.opponents),
                                 colour_hist=tuple(p.colour_hist))
            player_class_list.append(distinct_player)
            player_class_dict[p.pairing_no] = p.name         
        
    player_class_tuple = tuple(player_class_list)
    
    current_pairing = engine.pair_round(round_no, player_class_tuple)

    #現在のペアリングをDBに入れる
    for cp in current_pairing:
        q = CurrentRoundPlayerList.objects.filter(name = cp.name).get()
        q.score = cp.score
        q.float_status = cp.float_status
        q.opponents = list(cp.opponents)
        q.colour_hist = list(cp.colour_hist)
        
        q.save()
    
    #デバッグ用
    pairing_string = "------Round %d------\n\n" % round_no
        
    for cp in current_pairing:
        if cp.colour_hist[-1] is Colour.white:
            pairing_string += "No.%s\t%s - No.%s\t%s\n" % (cp.pairing_no,cp.name,
                                                         cp.opponents[-1],player_class_dict[cp.opponents[-1]])
        elif cp.colour_hist[-1] is Colour.none:
            pairing_string += "No.%s\t%s - Bye\n"% (cp.pairing_no,cp.name)
    print(pairing_string)
    #ここまで


def report_result(name, result):
    #名前と結果を投入する
    q = CurrentRoundPlayerList.objects.filter(name = name).get()
    q.score += result
    q.save()


def update_round():
    round = Round.objects.get()
    round.round_no += 1
    round.save()


if __name__ == "__main__":
    create_initial_players()
    show_pairing()
    report_result('Shiki',1)
    report_result('Kanade',0)
    report_result('Frederica',1)
    report_result('Mika',0)
    report_result('Rin',0.5)
    report_result('Shuko',0.5)
    report_result('Nao',1)
    report_result('Karen',0)
    update_round()
    show_pairing()