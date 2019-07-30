# sort_nazonazo

## 動作確認をした環境

python 3.7.2

discord.py 1.2.3

Ubuntu 16.04.6 LTS

## bot の動かし方

channel_id, token ファイルの設定が必要です。

./key/. に discord の bot 用 token を置きます。
ファイル名は token とし、トークンの文字列のみを持つようにして下さい。

bot が動作するチャンネルを指定する必要があります。
bot がいるサーバーの、動かしたいチャンネルの ID のみを持つファイルを
同様に ./key/. にファイル名を channel_id として置いて下さい。

run.sh で実行します。

## 辞書の追加

辞書が追加できます。

"問題の答え" "問題"

となるように辞書を作って ./dics/. に追加し、
./src/dictionary_list にファイル名を追加して下さい。

詳しくは既存の 8moji.dic, dictionary_list を見ていただければと思います。
