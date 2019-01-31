

def validate_tournament_info(tournament_info):
    is_validated = True
    player_name = []
    for p in tournament_info["playerlist"]:

        #重複チェック    
        if p["name"] in player_name:
            is_validated = False
                    
        #空文字チェック
        if len(p["name"]) is 0:
            is_validated = False
        else:
            player_name.append(p["name"])
        
        #数値変換チェック
        if p["rating"].isdigit() is False:
            is_validated = False
    
    return is_validated