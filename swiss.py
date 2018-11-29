from swissdutch.dutch import DutchPairingEngine
from swissdutch.constants import FideTitle, Colour, FloatStatus
from swissdutch.player import Player

import csv
import copy

class Tournament():

    def __init__(self):
        self.player_class_tuple = None
        self.round = 1
        self.engine = DutchPairingEngine()
        self.pairing_nos = {}
        self.current_pairing = None

        self.pooled_results ={}


    def _read_from_csv(self, filename):
        ret = []
        with open(filename, "r") as f:
            reader = csv.reader(f,delimiter=",", lineterminator="\n")
            header = next(reader)
            for r in reader:
                ret.append(r)
            return ret


    def create_initial_players(self, filename):
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
        self.current_pairing = self.engine.pair_round(self.round, self.player_class_tuple)

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
        result_dict = {"white_name": white_name,
                        "white_result": white_result,
                        "black_name": black_name,
                        "black_result": black_result}
        self.pooled_results[white_name] = white_result
        self.pooled_results[black_name] = black_result

    def update_round(self):
        update_player_class_list = []
        for cp in self.current_pairing:
            if cp.colour_hist[-1] is Colour.none:
                up = Player(name=cp.name,
                        rating=cp.rating,
                        pairing_no = cp.pairing_no,
                        score=cp.score,
                        float_status=cp.float_status,
                        opponents = cp.opponents,
                        colour_hist = cp.colour_hist)
                print(up)
            else:
                up = Player(name=cp.name,
                        rating=cp.rating,
                        pairing_no = cp.pairing_no,
                        score=cp.score + self.pooled_results[cp.name],
                        float_status=cp.float_status,
                        opponents = cp.opponents,
                        colour_hist = cp.colour_hist)
                print(up)
            update_player_class_list.append(up)

        self.player_class_tuple = tuple(update_player_class_list)
        self.pooled_results = {}
        self.round += 1
        return

if __name__ == "__main__":
    tn = Tournament()
    tn.create_initial_players("initialplayerlist.csv")

    # round 1
    tn.show_pairing()
    tn.report_result(white_name="yukari", white_result=1, black_name="shiki", black_result=0)
    tn.report_result(white_name="shiho", white_result=1, black_name="antilles", black_result=0)
    tn.report_result(white_name="kanade", white_result=0, black_name="honoka", black_result=1)

    tn.update_round()

    #round 2
    tn.show_pairing()
    tn.report_result(white_name="shiho", white_result=1, black_name="naho", black_result=0)
    tn.report_result(white_name="yukari", white_result=0.5, black_name="honoka", black_result=0.5)
    tn.report_result(white_name="kanade", white_result=0, black_name="shiki", black_result=1)

    tn.update_round()

    #round 3
    tn.show_pairing()
