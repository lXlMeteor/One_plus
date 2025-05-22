# Discord bot 「One_Plus(仮)」
One_Plus(仮)は、Discordで用いるbotのひとつです。
他のBotではない機能、少し足りない機能を補うことができることを目指して開発しています。

制作者：ふる公(関西大学総合情報学部公認団体Versear所属)

制作期間：2024年10月～開発中

使用技術：Python(Flask), PostgreSQL

OS：Windows11


## 概要
### 制作目的
Discordは、様々存在するチャットアプリケーションの一つですが、他のチャットアプリケーションにはある機能がDiscordにはないことがあります。
また、Discordには様々なbotが存在する中で、未だに機能として実装されていなかったり、使いにくい機能が様々存在します。
その「便利なんだけれども少し足りない」を解決するために、One_Plusを開発しています。
基本的に、有名なDiscordのBotに実装されている機能は実装しないようにしています。(もしかしたら調べ不足で入っているかもしれません...)
他にはなくて、でもあったら少し面白い機能、楽しい機能、便利な機能を実装していきます。

## 環境
### 前提
本プロダクトはローカル環境で環境構築を行ったため、Dockerが存在していません。今学期中にはDockerを作成する予定です。

ですので、実行する場合はvenv環境での実行をおすすめします。
pip installする必要があるライブラリは以下の通りです。

・discord.py

・dotenv

・datetime

・sqlalchemy

・asyncio

・requests

・googletrans

・langdetect

・psycopg[binary]

また、PostgreSQLも用いています。ユーザ名、パスワード等は.envにて、各自の値に設定してください。

### 実行
Linux/Mac OS の場合：
```python3 bot.py```

Windowsの場合：
```py bot.py```