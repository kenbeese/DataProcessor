[![Build Status](https://travis-ci.org/kenbeese/DataProcessor.png)](https://travis-ci.org/kenbeese/DataProcessor)

        ___      _          ___
       /   \__ _| |_ __ _  / _ \_ __ ___   ___ ___  ___ ___  ___  _ __
      / /\ / _` | __/ _` |/ /_)/ '__/ _ \ / __/ _ \/ __/ __|/ _ \| '__|
     / /_// (_| | || (_| / ___/| | | (_) | (_|  __/\__ \__ \ (_) | |
    /___,' \__,_|\__\__,_\/    |_|  \___/ \___\___||___/___/\___/|_|

Make your data analysis easy.

数値計算では多くの計算を実行するため、
どのような環境でどの計算を行なったか分からなくなります。
このプロジェクトは膨大な計算の管理を補助するためのものです。

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc/generate-toc again -->
**Table of Contents**

- [何ができるの？](#何ができるの？)
- [Tutorial (Linux/OS X)](#tutorial-linux/os-x)
    - [インストール](#インストール)
        - [既存の計算のスキャン](#既存の計算のスキャン)
            - [`scan_directory`を使用する場合](#scan_directoryを使用する場合)
            - [`add_run`を使用する場合](#add_runを使用する場合)
        - [計算のパラメータの読み込む](#計算のパラメータの読み込む)
            - [方法1](#方法1)
            - [方法2](#方法2)
    - [使い方](#使い方)
        - [一覧の表示(webapp)](#一覧の表示webapp)
        - [新しい計算の追加](#新しい計算の追加)
        - [コメント追加](#コメント追加)
        - [タグの追加と取り外し](#タグの追加と取り外し)
        - [Pythonから使う](#pythonから使う)
        - [お試し](#お試し)
    - [Lisence](#lisence)

<!-- markdown-toc end -->


何ができるの？
==============

- 個々の数値計算の設定、結果の一覧
- コメント、タグによる計算の整理
- 計算の開始(実験中)

もしあなたがpythonを使用してデータを解析しているならばさらに以下の機能が使えます。
- 計算の設定によるフィルタリング

Tutorial (Linux/OS X)
====================

インストール
------------

ダウンロードして依存関係のパッケージをインストールしてパスを通します。
以下ではホーム(`$HOME`)にインストールしますが、
環境に応じて変更してください。

```command
cd ~
git clone https://github.com/kenbeese/DataProcessor.git
cd DataProcessor
pip install -r requirements.txt # 依存関係のinstall
```

`~/.bashrc`の最後に以下の行を追加してパスを通します。
zsh等を使用している場合は`~/.zshrc`等に読みかえて下さい。

```bash
export PATH=$PATH:$HOME/DataProcessor/bin
export PYTHONPATH=$PYTHONPATH:$HOME/DataProcessor/lib
```

zshを使用している場合は各種コマンドの補完を有効にするため以下を設定します。

```zsh
export FPATH=$FPATH:$HOME/DataProcessor/zsh_completion
```

さらにDataProcessorの設定ファイル`~/.dataprocessor.ini`を生成します。

```command
dpinit
```

を起動すると、
DataProcessorのホームディレクトリと、計算の情報を保持するJSONファイルのパスを聞かれます。
これに答えればインストールは完了です。

### 既存の計算のスキャン

おそらくあなたは既に多くの計算を実行し、
独自の方法でその管理を行なっているでしょう。
ここではそれらの計算をDataProcessorで管理する準備をします。

以下で2通りの方法を説明します。

#### `scan_directory`を使用する場合
この作業は以下の事を仮定します。
- 計算とディレクトリが一対一対応している
- そのディレクトリに特定の名前のファイルがある

この条件を満している場合は`scan_directory`を使用する事ができます。

```command
dpmanip -s scan_directory /path/of/root/directory "*.ini"
```

`/path/of/root/directory`は計算に対応するディレクトリの親ディレクトリを指定します。
このディレクトリ以下を再帰的にスキャンして管理下に置きます。
もし複数に分れている時は複数回呼びます。

```command
dpmanip -s scan_directory /main/path/of/root/directory "*.ini"
dpmanip -s scan_directory /another/path/of/directory "*.ini"
```

最後の引数`"*.ini"`は見つけたディレクトリが計算と
対応しているディレクトリがどうかを判定するために使います。
もし`"*.ini"`に一致するファイルがある場合はそのディレクトリを
計算に対応しているディレクトリとして扱います。

#### `add_run`を使用する場合

上記の条件を満たしていない場合、各ランのディレクトリを個別に登録します。

```command
dpmanip -s add_run /path/to/run
```

で登録できます。

同時にtag、commentや別名を残したい場合は

```command
dpmanip -s add_run /path/to/run --tag tagname_or_projectpath --name run_run_run --comment "The best run."
```

で出来ます。tagやcommentは後からでも下に記述してあるように、
`add_tag`, `add_comment`で追加できます。


### 計算のパラメータの読み込む
上述の作業ではまだ計算とディレクトリを対応させただけです。
次に個々の計算のパラメータを登録します。


#### 方法1

もし計算のディレクトリに設定ファイルがINI形式で保存されていれば
```command
dpmanip -s configure conf.ini
```

`conf.ini`はINIファイルの名前に変更してください。
セクションのないINIファイル

```
A = 1
B = 1.0
C = 2.0
```

のような場合には

```command
dpmanip -s configure_no_section conf.ini
```

で可能です。

#### 方法2
設定ファイルが独自形式の場合、各ランのパラメータを

```command
dpmanip -s add_conf /path/to/run a 1
dpmanip -s add_conf /path/to/run b 1.0
dpmanip -s add_conf /path/to/run c 2.0
```

で登録可能です。

使い方
------
### 一覧の表示(webapp)

計算の設定の一覧を表示するには`dpserver`によってサーバープロセスを起動する必要があります。
初回の起動の前に以下のコマンドを実行する必要があります：

```command
dpserver install
```

サーバープロセスは以下のコマンドで起動します：

```command
dpserver start
```

特に指定しない場合、8080番のportを使用します。
[http://localhost:8080/](http://localhost:8080/)を開けばプロジェクトの一覧が表示され、
その名前をクリックすると計算の一覧が表示されます。

サーバーを終了するには

```command
dpserver stop
```

とします。

### 新しい計算の追加
[`add_run`を使用する場合](#add_runを使用する場合)に書いてある通り、

```command
dpmanip -s add_run /path/to/run --tag tagname --comment "comment comment"
```

で追加できます。

### コメント追加

計算にコメントを追加するには[webapp](http://localhost:8080/)を使用する方法と
`dpmanip`を使用する方法があります。
webappではコメント覧をクリックするとコメントが入力できます。
フォーカスが外れると変更が保存されます。

`dpmanip`は以下の様にして使います：

```command
dpmanip -s add_comment "comment" /path/of/run
```

`"comment"`にはコメントしたい文字列を、
`/path/of/run`にはコメントしたい計算のpathを入力します。
現在のディレクトリの計算にコメントを付けるには

```command
dpmanip -s add_comment "comment" .
```

とします。

### タグの追加と取り外し

計算にタグを付ける事ができます。
タグは内部的にはプロジェクトと同じなので、
webappのプロジェクトのリストにタグも一緒に一覧されます。

```command
dpmanip -s add_tag /path/of/run "tagname"
```

`"tagname"`の替りに存在しているプロジェクトのパスを書く事もできます。

```command
dpmanip -s add_tag /path/of/run /path/of/project
```

tagは以下のコマンドで外せます。

```command
dpmanip -s untag /path/of/run tagname
```

or

```command
dpmanip -s untag /path/of/run /path/of/project
```

### Pythonから使う
(かきかけ)
[API reference](http://kenbeese.github.io/DataProcessor/index.html)

#### `dataprocessor.gencompletion`の使い方

自作スクリプトの引数やオプションのパーサーに
python標準ライブラリーにある`argparse`を使えば、
zshの補完定義が簡単に作れます。


使い方は簡単。
設定し終わった`argparse.ArgumentParser`のインスタンスを
`dataprocessor.gencompletion.CompletionGenerator`に渡すだけ。


以下はpypiにあるautopep8の補完を作成する場合

```python
#! /usr/bin/env python

import dataprocessor as dp
import autopep8

def main():
    parser = autopep8.create_parser() # argument parserのスクリプト作成
    comp = dp.gencompletion.CompletionGenerator("autopep8", parser)
    print comp.get()

if __name__ == "__main__":
    main()
```

### お試し
いきなり使うのは怖い場合はお試し用のデータディレクトリが`sample`にあります。
詳しい使い方は[ここ](sample/sample_usage.md)。

Lisence
-------
GPLv3
