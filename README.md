# sort_nazonazo

## 動作確認をした環境

python 3.7.2

discord.py 1.2.3

## bot の動かし方

channel_id, token ファイルの設定が必要です。

sort_nazonazo_bot.py がある場所と同じディレクトリに discord の bot 用 token を置きます。
ファイル名は token とし、トークンの文字列のみを持つようにして下さい。

bot が動作するチャンネルを指定する必要があります。
bot がいるサーバーの、動かしたいチャンネルの ID のみを持つファイルを
同様に sort_nazonazo_bot.py がある場所と同じディレクトリにファイル名を channel_id として置いて下さい。

run.sh で実行します。

## 辞書の追加

辞書が追加できます。

"問題の答え" "問題"

となるように辞書を作って sort_nazonazo_bot.py と同じディレクトリに追加し、
dictionary_list にファイル名を追加して下さい。

詳しくは既存の 8moji.dic, dictionary_list を見ていただければと思います。
