from django.conf import settings
import sys, os
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiss.settings")
import django
django.setup()

from swissdutch.dutch import DutchPairingEngine
from swissdutch.constants import FideTitle, Colour, FloatStatus
from swissdutch.player import Player

import pickle
import csv
import copy
import sys
from swiss_gui.models import InitialPlayerList,ParticipatedPlayerList
from swiss_gui.models import CurrentRoundPlayerList,Round,PooledResults,ResultsHistory,PickledEngine

from swiss_gui.exception.swiss_exception import SwissException
from swiss_gui import constants

#トーナメント開始時に呼ばれる
def create_initial_players():
    #プレーヤーリストを、swiss_gui_participatedplayerlistテーブルに登録する。
    if len(InitialPlayerList.objects.order_by('rating').reverse().all()) > 1:
        players = InitialPlayerList.objects.order_by('rating').reverse().all()
    else:
        raise SwissException("Initial player number must be more than 1.")
    
    #もともと入っていたレコードを消す
    ParticipatedPlayerList.objects.all().delete()
    CurrentRoundPlayerList.objects.all().delete()
    PooledResults.objects.all().delete()
    Round.objects.all().delete()
    ResultsHistory.objects.all().delete()
    PickledEngine.objects.all().delete()
    
    #swiss_gui_initialplayerlistテーブルから追加する。
    for i, player in enumerate(players):
        q = ParticipatedPlayerList(
            name = player.name,
            rating = player.rating,
            pairing_no = i+1,
            score = 0,
            float_status = 0,
            tiebreak_score=0
            )
        q.save()
        q = CurrentRoundPlayerList(
            name = player.name,
            rating = player.rating,
            pairing_no = i+1,
            score = 0,
            float_status = 0,
            tiebreak_score=0
            )
        q.save()
    
    q = Round(round_no = 1)
    q.save()
    
    return

#次ラウンド開始時に呼ばれる
def create_pairing():
    #現在のラウンド数を取得する
    round_no = Round.objects.get().round_no
    if round_no is 1:
        #最初のラウンドは、Engineを作成する
        engine = DutchPairingEngine()
    else:
        #2ラウンド以降は、pickle化したエンジンを取得する
        engine = load_engine()
    
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
            if (len(p.opponents) is not round_no - 1) or (len(p.colour_hist) is not round_no - 1):
                raise SwissException("Round No. must be wrong.")
            
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
    
    #engineをダンプする
    dump_engine(engine)
    
    #現在のペアリングをDBに入れる
    for cp in current_pairing:
        if not len(CurrentRoundPlayerList.objects.filter(name = cp.name)) is 1:
            raise SwissException("CurrentRoundPlayerList must be wrong.")
        
        q = CurrentRoundPlayerList.objects.filter(name = cp.name).get()
        q.score = cp.score
        q.float_status = cp.float_status
        q.opponents = list(cp.opponents)
        q.colour_hist = list(cp.colour_hist)
        
        q.save()
        
        #Byeのプレーヤーは、PooledResultをこのタイミングで入れておく
        if cp.colour_hist[-1] is Colour.none:            
            q = PooledResults(name=cp.name,result=1)
            q.save()
    
def report_result(name, result):
    #名前と結果を投入する
    q = CurrentRoundPlayerList.objects.filter(name = name).get()
    q.score += result
    q.save()
    q = PooledResults(name=name,result=result)
    q.save()

    
def report_results(white_name, white_result, black_name, black_result):
    #エラーチェック。白の結果が入っていないときに黒の結果を入れないようにする
    validate = validate_result(white_name, white_result, black_name, black_result)
    #結果のバリデーション。
    if validate is 0:
        report_result(white_name, white_result)
        report_result(black_name, black_result)
        
        #結果をResultsHistoryテーブルに投入する
        q = ResultsHistory(
            round = Round.objects.all().get().round_no,
            white_no = ParticipatedPlayerList.objects.filter(name=white_name).get().pairing_no,
            white_name = white_name,
            white_result = white_result,
            black_no = ParticipatedPlayerList.objects.filter(name=black_name).get().pairing_no,
            black_name = black_name,
            black_result = black_result  
            )
        q.save()
        message = "Result Successfully updated!"
    else:
        message = "Result Update Failed"
    
    return {"message":message}


def validate_result(white_name, white_result, black_name, black_result):
    validate = 0
    #白と黒の結果を足して1にならなければ、不正
    if not white_result + black_result == 1:
        validate = 1
    #もし、名前がDBになければ、不正
    if len(CurrentRoundPlayerList.objects.filter(name = white_name)) is not 1:
        validate = 1
    else:
        opponent_no = CurrentRoundPlayerList.objects.filter(name = white_name).get().opponents[-1]
        if len(CurrentRoundPlayerList.objects.filter(pairing_no = opponent_no)) is not 1:
            validate = 1
        else:
            if not CurrentRoundPlayerList.objects.filter(pairing_no = opponent_no).get().name in [black_name,]:
                validate = 1
    
    return validate


#次ラウンド移行時に呼ばれる
def update_round():
    
    if len(PooledResults.objects.all()) is len(CurrentRoundPlayerList.objects.all()):
        round = Round.objects.get()
        round.round_no += 1
        PooledResults.objects.all().delete()
        round.save()
        
        #Buchholz法でのタイブレーク計算
        for crp in CurrentRoundPlayerList.objects.all():
            
            crp.tiebreak_score = tiebreak_sb(crp)
            crp.save()
        
        return {"can_update":1, "message":"Round %s pairing successfully created!" % round.round_no}
    else:
        return {"can_update":0, "message":"Results are not fully reported."}


def tiebreak_sb(crp):
    tiebreak = 0
    opponents = crp.opponents
    for opponent in opponents:
        if not opponent is 0:
            tiebreak += CurrentRoundPlayerList.objects.filter(pairing_no=opponent).get().score
    return tiebreak


def dump_engine(engine):
    pickled_engine = pickle.dumps(engine)
    
    if len(PickledEngine.objects.all()) is 0:
        q = PickledEngine(pickled_engine = pickled_engine)
        q.save()
    elif len(PickledEngine.objects.all()) is 1:
        q = PickledEngine.objects.all().get()
        q.pickled_engine = pickled_engine
        q.save()
    else:
        raise SwissException("there exist  more than 1 pickled engines!")

def load_engine():
    if len(PickledEngine.objects.all()) is 1:
        engine = pickle.loads(PickledEngine.objects.all().get().pickled_engine)
    else:
        raise SwissException("Engine cannot be unpickled.")
    return engine


if __name__ == "__main__":
    create_initial_players()
    show_pairing()