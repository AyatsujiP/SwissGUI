# スイス式トーナメントペアリング補助ツール

## 使い方

- 以下のように使う。

### 事前準備
    tn = Tournament()
    tn.create_initial_players("initialplayerlist.csv")
    
    
### 1ラウンドの流れ
    tn.show_pairing()
    tn.report_result(white_name="Kasparov", white_result=1, black_name="Kramnik", black_result=0)
    ...
    ...
    (必要分だけ)
    
    tn.update_round()
    
    
    
    