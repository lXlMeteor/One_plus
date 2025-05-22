#チャンネル内チャットログ化機能

from datetime import timedelta
import os, json, discord

import Component.component_def as component_def

async def summary_all(ctx, bot):

    await component_def.defer(ctx)

    async for message in ctx.channel.history(limit=1):
        data = message
        break 
    channel_id = data.channel.id

    channel = bot.get_channel(channel_id)

    messages = []

    async for message in channel.history(limit=None):  # limit=Noneで全メッセージ取得
        print(message.content)
        if (message.content is None or message.content == " ") and message.attachments is None:
            continue
        messages.append({"user":str(message.author), 
                         "message":message.content,
                         "datetime":(message.created_at + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
                        })

    with open('txt/test.txt', 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

    await ctx.followup.send(file=discord.File('txt/test.txt'))
    os.remove('txt/test.txt')