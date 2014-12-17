Sample
======

とりあえず、使ってみましょう。
そのために、お試し環境を作成しましょう。

お試し環境の作成
----------------

### 設定ファイルの作成

```command
dpinit
```

rootdirにはこのサンプルディレクトリの"datadir"を指定します。
json fileの場所は適当に設定してください。


既に設定ファイルを作成していた場合はちゃんとバックアップを取ってね。
この場合、バックアップしてた`.dataprocessor.ini`をHOMEに置けば、
元のデータベースが使えます。

### データのスキャン

datadir以下にあるファイルは以下の通りです。

- datadir/project1/run01/parameters.conf: run parameter file
- datadir/project1/run03/parameters.conf: run parameter file
- datadir/project2/run01/parameters.ini: run parameter file
- datadir/project2/run02/parameters.ini: run parameter file
- datadir/project2/run03/parameters.conf: run parameter file

これらのrunをScanしましょう

```sh
dpmanip -s scan_directory /path/to/datadir "parameters.ini"  # parameters.iniのファイルがあるディレクトリをランとして認識してscan
dpmanip -s scan_directory /path/to/datadir "*.conf" # 拡張子.confのファイルがあるディレクトリをランとして認識してscan
```

or

```sh
dpmanip -s scan_directory /path/to/datadir "*.ini" "parameters.conf" # 拡張子.ini or parameters.confのファイルがあるディレクトリをランとして認識してscan
```

スキャンした結果を表示してみる

```sh
dpmanip -s show_runs
dpmanip -s show_projects
```

### 設定ファイルのスキャン

```sh
dpmanip -s configure parameters.conf # parameters.confがあるrunで、このファイルを読み込む
dpmanip -s configure parameters.ini  # parameters.iniがあるrunで、このファイルを読み込む
```

スキャンした結果を表示してみる

```sh
dpmanip -s show_runs --parameters nx
```

遊んでみよう
------------

上記で作成した環境なら壊しても問題ないので、
色々`dpmanip`と`dpserver`を使って遊んでみよう。

dpmanipのサブコマンドリストは以下のコマンドで見れるぞ。

```sh
dpmanip -h
```
