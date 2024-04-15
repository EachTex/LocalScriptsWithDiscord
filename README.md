# LocalScriptsWithDiscord
Discordでローカル環境のスクリプトを視覚的に操作するプログラムです。

# Notes:
現行の開発/実装環境は最新のバージョンではないものを使用しています。  
これらのコードを使用することは問題ありませんが、  
各人のプログラムに組み込む際は、最新のバージョンに合わせてコードを変更してください。
### Requirements.txt
```py
discord.py==2.0.1
py-cord==2.5.0
```

# Usage:
[ソースコード](https://github.com/EachTex/LocalScriptsWithDiscord/blob/main/cog.py)をCogsフォルダに追加し、  
ボットホスト用サーバーで [サーバースクリプト](https://github.com/EachTex/LocalScriptsWithDiscord/blob/main/server_localtonet.py)を実行してください。
また、カレントディレクトリ内に  
- "localnet.json" (\*接続データを保存するファイル)  
を作成してください。
その後、[クライアントスクリプト](https://github.com/EachTex/LocalScriptsWithDiscord/blob/main/client_localtonet.py)を実行すると、Discordとローカルでのスクリプトを接続できます。
(参考: [Twitter (X)](https://x.com/xMasa1022/status/1779776184156602645))

※このコードは開発者の考案した作品を無理やり実現させたもので、可読性，利便性などを一切無視して作成しました。  
このコードを実行したことによる不具合等は一切責任を負いません。
