# スイス式トーナメントペアリング補助ツール

## 使い方

- 以下のように使う。

### 事前準備
1． PostgreSQL上に、以下のデータベース、ロールを準備
- ロール
     + ユーザ名 swiss
     + パスワード swiss

- データベース
     + データベース名 swiss_gui
     + オーナー swiss

2. マイグレートを実施
コマンドライン上でmanage.pyがあるディレクトリに移動し、以下を実行

~~~python
      python3 manage.py makemigrations swiss_gui
      python3 manage.py makemigrations
      python3 manage.py migrate
~~~

3. 実行
    python3 manage.py runserver
    
- http://127.0.0.1:8000/で実行される。


### トーナメントの実施方法
  トップ画面のCreate New Tournamentをクリック
 参加するプレーヤーの一覧は、事前に`swiss_gui_initialplayerlist`テーブルに投入しておく(投入部分は、未GUI化だがGUI化予定あり)
1. Start Tournamentをクリック
 
1. ペアリングが自動生成されるので、ペアリングに従ってゲームを実施
1. 結果は、Report画面から投入する
1. 全ての結果を投入したところで、Go to Next Roundボタンをクリックすると、次ラウンドに移行すると、ペアリングが自動生成される
1. 以下、2-4を繰り返す
1. 予定していた全ラウンドが終わったら、End Tournamentをクリック

### 既知のバグ
 - 人数に対してラウンド数が多い時に、ペアリングが生成されないことがある(対処中。現在発見している限りでは、8人に対して4ラウンドを組もうとすると起きる。)

### WSGI Setup
 - /var/www/以下にチェックアウトして/etc/apache2/apache2.confに以下を追加すると、Apacheからホストできる。

~~~
      LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so
      WSGIScriptAlias / /var/www/SwissGUI/swiss/wsgi.py
      <Directory /var/www/SwissGUI/swiss>
          <Files wsgi.py>
              Require all granted
          </Files>
      </Directory>
~~~

