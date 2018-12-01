from swissdutch.dutch import DutchPairingEngine
from swissdutch.constants import FideTitle, Colour, FloatStatus
from swissdutch.player import Player

import csv
import copy
import sys
from swiss_gui.models import  InitialPlayerList,ParticipatedPlayerList,CurrentRoundPlayerList,Round,PooledResults

class Tournament():
    """
    1つのトーナメントは、Tournamentクラスのインスタンスを作ることで管理される。
    """

    def __init__(self):
        #Playerクラスの順序付きタプル。
        self.player_class_tuple = None
        #現在のラウンド数を、状態として持っている。
        self.round = 1
        #エンジン
        self.engine = DutchPairingEngine()
        #ペアリングナンバーと、プレーヤー名の辞書。Playerクラスのタプルだと検索が難しいため作っておく。
        self.pairing_nos = {}
        #現在のラウンド数におけるペアリング。
        self.current_pairing = None
        #「現在のラウンド」ですでに終了した結果をプールしておくための変数。
        self.pooled_results ={}


    def _read_from_csv(self, filename):
        #CSVファイルから、プレーヤーリストを読み込む。
        #プレーヤーリストは、レーティング順に並べておくこと。
        ret = []
        with open(filename, "r") as f:
            reader = csv.reader(f,delimiter=",", lineterminator="\n")
            header = next(reader)
            for r in reader:
                ret.append(r)
            return ret


    def create_initial_players(self, filename):
        #読み込んだプレーヤーリストから、swissdutchライブラリに取り込み可能なように、タプルを作成する。
        player_list = self._read_from_csv(filename)
        player_class_list = []
        for i, pl in enumerate(player_list):
            distinct_player = Player(name=pl[0],
                                     rating=pl[1],
                                     pairing_no = i+1,
                                     score=0,
                                     float_status=FloatStatus.none)
            player_class_list.append(distinct_player)
            self.pairing_nos[i+1] = pl[0]

        self.player_class_tuple = tuple(player_class_list)
        return


    def show_pairing(self):
        #ペアリングを組む。
        self.current_pairing = self.engine.pair_round(self.round, self.player_class_tuple)
        #ペアリングを表示する。「白番-黒番」で表示し、Byeは個別に表示する。
        pairing_string = "------Round %d------\n\n" % self.round
        
        for cp in self.current_pairing:
            #print (cp.colour_hist[-1])
            if cp.colour_hist[-1] is Colour.white:
                pairing_string += "No.%s\t%s - No.%s\t%s\n" % (cp.pairing_no,cp.name,cp.opponents[-1],self.pairing_nos[cp.opponents[-1]])
            elif cp.colour_hist[-1] is Colour.none:
                pairing_string += "No.%s\t%s - Bye\n"% (cp.pairing_no,cp.name)

        print(pairing_string)


    def report_result(self, *,
            white_name, white_result, black_name, black_result):
        #結果を、関数の引数として投入する。「白の名前」「白の結果(0,0.5,1)」「黒の名前」「黒の結果」の順。
        #結果は、pooled_resultsにプールされる。
        result_dict = {"white_name": white_name,
                        "white_result": white_result,
                        "black_name": black_name,
                        "black_result": black_result}
        self.pooled_results[white_name] = white_result
        self.pooled_results[black_name] = black_result

    def update_round(self):
        #プールされた結果を用いて、次のペアリングを生成する。
        update_player_class_list = []
        #現在のラウンドの結果を反映したPlayerクラスのインスタンスを、プレーヤーの数ぶんだけ生成する。
        for cp in self.current_pairing:
            if cp.colour_hist[-1] is Colour.none:
                #Byeの場合
                up = Player(name=cp.name,
                        rating=cp.rating,
                        pairing_no = cp.pairing_no,
                        score=cp.score,
                        float_status=cp.float_status,
                        opponents = cp.opponents,
                        colour_hist = cp.colour_hist)
                print(up)
            else:
                #Bye以外の場合
                up = Player(name=cp.name,
                        rating=cp.rating,
                        pairing_no = cp.pairing_no,
                        score=cp.score + self.pooled_results[cp.name],
                        float_status=cp.float_status,
                        opponents = cp.opponents,
                        colour_hist = cp.colour_hist)
                print(up)
            update_player_class_list.append(up)
        #タプルに変換し、ラウンドのカウントを1つ増やす。
        self.player_class_tuple = tuple(update_player_class_list)
        self.pooled_results = {}
        self.round += 1
        return

if __name__ == "__main__":
    tn = Tournament()
    tn.create_initial_players("initialplayerlist.csv")

    # round 1
    tn.show_pairing()