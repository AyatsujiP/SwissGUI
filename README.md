# Sugared Swiss Tournament Organizer V1.1.1


## 説明
- 本ツール(以下Sugared STO)は、Python 3系で動作する、スイス式トーナメントのペアリングを自動生成するツールである。
- 以下のパッケージに依存する。これらはpipからインストールできるため、インストール手順は省略する。
    + swissdutch
    + django
    + psycopg2
- Windows 10, およびLinux(Lubuntu 16.04)で動作を確認している。

## Dockerを使わないインストール方法

以下のようにインストールする。

### 事前準備
1.PostgreSQL上に、以下のデータベース、ロールを準備
- ロール
     + ユーザ名 swiss
     + パスワード swiss

- データベース
     + データベース名 swiss_gui
     + オーナー swiss

2.マイグレートを実施

コマンドライン上でmanage.pyがあるディレクトリに移動し、以下を実行

~~~python
      python3 manage.py makemigrations swiss_gui
      python3 manage.py makemigrations
      python3 manage.py migrate
~~~

3.ユーザ作成

以下のコマンドを実施。

~~~python
      python3 manage.py createsuperuser
~~~

実施後、ユーザ名、Eメール(任意)、パスワードを入力するプロンプトが現れるので、
このアプリケーションで使うユーザ名とパスワードを入力する。

4.実行

Webサーバを開始して実行

~~~python
    python3 manage.py runserver
~~~
    
127.0.0.1:8000で実行される。


### Docker版のインストール方法
Sugered STOは、Dockerでのデプロイにも対応している。

Docker自体のインストール方法は割愛する。
dockerディレクトリ配下にあるDockerfileと、supervisord.confを、デプロイしたいマシンのディレクトリに格納し、そのディレクトリに移動したのちに
以下のコマンドを(dockerコマンドが使える権限のユーザで)入力すること。

(ソースコードはDockerfile内でcloneしてくるため、デプロイは不要である。
2ファイルだけおけばよいので、簡単にデプロイできる。)

~~~bash
    docker build -t sugar_sto .
    docker run -it -p 8000:8000 sugar_sto:latest
~~~

入力したのちに、Dockerホスト側のマシンで、127.0.0.1:8000にアクセスすれば使用可能である。



### トーナメントの実施方法
 トップ画面のCreate New Tournamentをクリック
1. Start Tournamentをクリック
1. ペアリングが自動生成されるので、ペアリングに従ってゲームを実施
1. 結果は、Report画面から投入する
1. 全ての結果を投入したところで、Go to Next Roundボタンをクリックすると、次ラウンドに移行すると、ペアリングが自動生成される
1. 以下、2-4を繰り返す
1. 予定していた全ラウンドが終わったら、End Tournamentをクリック
1. ゲーム終了後、左のメニューからDownload TRFをクリックするとTRFファイルが出力される

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

## リリースノート
 - 2019/1/31 Ver1.0.0公開
 - 2019/2/10 Ver1.1.0公開
      + ライセンス表記追加(MIT)
    + TRFファイル出力対応
     + ボード番号出力に対応
 - 2019/2/10 Ver1.1.1公開
     + ディレクトリを整理