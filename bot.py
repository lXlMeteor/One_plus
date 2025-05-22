
# -*- coding: utf-8 -*-
import discord, logging, os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

import Component.component_timestamp as component_timestamp, Component.component_help as component_help,\
       Component.component_blackjack as component_blackjack, Component.component_draft as component_draft,\
       Component.component_rps as component_rps, Component.component_pin as component_pin,\
       Component.component_summary as component_summary, Component.component_dicepoker as component_dicepoker,\
       Component.component_coin as component_coin, Component.component_translate as component_translate, \
       Component.component_remind as component_remind, Component.component_outpro as component_outpro


intents = discord.Intents.all()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix="/", intents=intents)

load_dotenv()

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

class ColorChoice(app_commands.Choice[str]):
    pass


#ブラックジャック
@bot.tree.command(name="blackjack", description="ブラックジャックをプレイします")
async def blackjack(ctx: discord.Interaction):

    await component_blackjack.blackjack(ctx)

@bot.tree.command(name="coin_blackjack", description="入力された枚数のコインを賭けてブラックジャックをプレイします、初めてプレイする方にはコイン100枚が与えられます")
async def coin_blackjack(ctx: discord.Interaction, coin:int):

    await component_blackjack.coin_blackjack(ctx, coin)

@bot.tree.command(name="blackjack_help",description="ブラックジャックのルールを確認します")
async def blackjack_help(ctx: discord.Interaction):

    await component_blackjack.blackjack_help(ctx)

@bot.tree.command(name="dicepoker", description="ダイスポーカーをプレイします")
async def dicepoker(ctx: discord.Interaction):
    
    await component_dicepoker.dicepoker(ctx)

@bot.tree.command(name="coin_check", description="あなたが今持っているコインの枚数を表示します")
async def coin_check(ctx: discord.Interaction):

    await component_coin.coin_check(ctx)


#下書機能
@bot.tree.command(name="draft_save", description="下書きを保存します。下書きは2000文字までを3つ保存できます")
async def draft_save(ctx: discord.Interaction, text:str):

    await component_draft.draft_save(ctx, text)

@bot.tree.command(name="draft_check", description="下書内容の最初の方を確認します。下書の内容を全て確認する場合は '/draft 番号' のコマンドを使用してください。")
async def draft_check(ctx: discord.Interaction):

    await component_draft.draft_check(ctx)

@bot.tree.command(name="draft", description="下書内容を確認します。'/draft_check'で番号を確認して、入力欄に番号を入力してください。")
async def draft(ctx: discord.Interaction, number:int):

    await component_draft.draft(ctx, number)

@bot.tree.command(name="draft_delete", description="下書内容を削除します。'/draft_check'で番号を確認して、入力欄に番号を入力してください。")
async def draft_delete(ctx: discord.Interaction, number:int):

    await component_draft.draft_delete(ctx, number)


#タイムスタンプ
@bot.tree.command(name="startstamp", description="会議開始時の日時を記録します")
async def startstamp(ctx: discord.Interaction):

    await component_timestamp.startstamp(ctx)
    
@bot.tree.command(name="endstamp", description="会議開始時の日時を記録します")
async def endstamp(ctx: discord.Interaction):

    await component_timestamp.endstamp(ctx)


#ピン留め
@bot.tree.command(name="pin",description="Discordのメッセージリンクによって、10個までピン留めを行います")
async def pin(ctx: discord.Interaction, url:str):

    await component_pin.pin(ctx, url, bot)

@bot.tree.command(name="pin_check",description="このサーバーでピン留めしたメッセージを全て表示します")
async def pin_check(ctx: discord.Interaction):

    await component_pin.pin_check(ctx, bot)

@bot.tree.context_menu(name="ピン留めする")
async def pin_menu(ctx: discord.Interaction, message: discord.Message):

    await component_pin.pin_menu(ctx, message)


#チャンネル履歴表示(txtファイルで出力)
@bot.tree.command(name="summary_all",description="このチャンネルのメッセージをすべて表示します")
async def summary_all(ctx: discord.Interaction):

    await component_summary.summary_all(ctx, bot)

#じゃんけん
@bot.tree.command(name="rps",description="Botとじゃんけんをします")
async def rps(ctx: discord.Interaction):

    await component_rps.rps(ctx)

#オンラインプログラム実行機能
@bot.tree.command(name="outpro", description="プログラムコードを実行します")
@app_commands.describe(
    file="プログラムファイルを添付してください",
    lang="言語を選択してください",
    text="入力値を入力してください")  
@app_commands.choices(lang=[
    app_commands.Choice(name="Python", value="python3"),
    app_commands.Choice(name="C言語", value="c"),
    app_commands.Choice(name="Java", value="java")
])
async def outpro(ctx: discord.Interaction, file: discord.Attachment, lang: app_commands.Choice[str], text:str = None):

    await component_outpro.outpro(ctx, lang, text, file)

#翻訳機能
@bot.tree.context_menu(name="日本語に翻訳する")
async def translate(ctx: discord.Interaction, message: discord.Message):

    await component_translate.translate(ctx, message)

#リマインド機能(未実装)
@bot.tree.context_menu(name="一日後にリマインド")
async def remind(ctx: discord.Interaction, message: discord.Message):
    
    await component_remind.remind_day(ctx, message)


#コマンド一覧
@bot.tree.command(name = "help", description="Botのコマンドを確認します")
async def help(ctx: discord.Interaction):
    
    await component_help.help(ctx, bot)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}')
    logging.info(f'Start bot at {datetime.now()}')

bot.run(os.getenv("KEY"))
