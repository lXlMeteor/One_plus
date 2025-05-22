#ブラックジャック(データ処理)

from dotenv import load_dotenv
import os

import Component.component_blackjack_game as component_blackjack_game, Component.component_def as component_def
import Button.button_blackjack as button_blackjack
import Database.crud_blackjack as crud_blackjack

load_dotenv()

def card_change(card):

    if card == 11:
        card = 'J'
    elif card == 12:
        card = 'Q'
    elif card == 13:
        card = 'K'
    elif card == 1:
        card = 'A'

    return card


async def blackjack(ctx):
    user_id, guild_id = await component_def.return_user_data(ctx)

    admin, challenger = component_blackjack_game.blackjack()
    challenger_score = component_blackjack_game.score_cal(challenger)

    card = card_change(challenger[0])
    admin_card = card_change(admin[0])

    text = f"あなたの最初のカードは {card} です。\n現在のスコア: {challenger_score}\nディーラーの最初のカードは{admin_card}です。"
    await ctx.response.send_message(text,view=button_blackjack.BlackjackView(user_id,admin,challenger))  # ボタンを表示

async def coin_blackjack(ctx, coin):
    await component_def.defer(ctx)

    user_id, guild_id = await component_def.return_user_data(ctx)

    user_coin = await crud_blackjack.check_coin(user_id, guild_id)

    if user_coin <= coin:
        text = "賭けているコインが、所持コイン数よりも大きいです"
        await component_def.followup_send_ephemeral(ctx, text)
        return
    elif coin <= 0:
        text = "コインは1枚以上を賭けてください"
        await component_def.followup_send_ephemeral(ctx, text)
        return

    admin, challenger = component_blackjack_game.blackjack()
    challenger_score = component_blackjack_game.score_cal(challenger)

    card = card_change(challenger[0])
    admin_card = card_change(admin[0])

    text = f"あなたの最初のカードは {card} です。\n現在のスコア: {challenger_score}\nディーラーの最初のカードは{admin_card}です。"
    await ctx.followup.send(text,view=button_blackjack.Coin_BlackjackView(user_id,admin,challenger,guild_id,coin)) 

async def blackjack_help(ctx):

    text = os.getenv("BLACKJACK_HELP")
    
    await component_def.message_response_ephemeral(ctx, text)