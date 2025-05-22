#じゃんけん機能

import Button.button_rps as button_rps

async def rps(ctx):

    text = "あなたの手を選択してください"
    await ctx.response.send_message(text,view=button_rps.RPSView(ctx.user.id))