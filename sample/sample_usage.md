Sample
======

とりあえず、使ってみましょう。
そのために、お試し環境を作成しましょう。
以下、DataProcessorを`$HOME`に置いた場合で話をすすめます。
違う場所に置いた場合は適宜読み変え下さい。

お試し環境の作成
----------------

### 設定ファイルの作成

```command
dpinit
```

rootdirには"$HOME/DataProcessor/sample/datadir"を指定します。
json fileの場所は適当に設定してください。


既に設定ファイルを作成していた場合はちゃんとバックアップを取ってね。
この場合、バックアップしてた`.dataprocessor.ini`をHOMEに置けば、
元のデータベースが使えます。

### データのスキャン

`$HOME/DataProcessor/sample/datadir`以下にあるファイルは以下の通りです。

- datadir/project1/run01/parameters.conf: run parameter file
- datadir/project1/run03/parameters.conf: run parameter file
- datadir/project2/run01/parameters.ini: run parameter file
- datadir/project2/run02/parameters.ini: run parameter file
- datadir/project2/run03/parameters.conf: run parameter file

これらのrunをScanしましょう

```sh
dpmanip scan_directory $HOME/DataProcessor/sample/datadir "parameters.ini"  # parameters.iniのファイルがあるディレクトリをランとして認識してscan
dpmanip scan_directory $HOME/DataProcessor/sample/datadir "*.conf" # 拡張子.confのファイルがあるディレクトリをランとして認識してscan
```

or

```sh
dpmanip scan_directory $HOME/DataProcessor/sample/datadir "*.ini" "parameters.conf" # 拡張子.ini or parameters.confのファイルがあるディレクトリをランとして認識してscan
```

スキャンした結果を表示してみる

```sh
dpmanip show_runs
dpmanip show_projects
```

### 設定ファイルのスキャン

```sh
dpmanip configure parameters.conf # parameters.confがあるrunで、このファイルを読み込む
dpmanip configure parameters.ini  # parameters.iniがあるrunで、このファイルを読み込む
```

スキャンした結果を表示してみる

```sh
dpmanip show_runs --parameters nx
```

遊んでみよう
------------

上記で作成した環境なら壊しても問題ないので、
色々`dpmanip`と`dpserver`を使って遊んでみよう。

dpmanipのサブコマンドリストは以下のコマンドで見れるぞ。

```sh
dpmanip -h
```
