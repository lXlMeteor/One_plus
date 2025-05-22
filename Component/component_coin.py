#コイン(サーバ内専用通貨)所持数

import Component.component_def as component_def
import Database.crud_blackjack as crud_blackjack


async def coin_check(ctx):

    user_id, guild_id = await component_def.return_user_data(ctx)
    
    credit = await crud_blackjack.check_coin(user_id, guild_id)
    
    text = f"あなたの所有しているコインの枚数は、{credit}枚です。"

    await component_def.message_response_ephemeral(ctx, text)