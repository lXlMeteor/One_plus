#ピン留め(個人)機能

import discord, asyncio, os
from datetime import datetime, timedelta
from functools import lru_cache
from dotenv import load_dotenv

import Component.component_def as component_def
import Database.crud_pin as crud_pin
import Button.button_pin as button_pin


load_dotenv()

@lru_cache(maxsize=128)  # キャッシュサイズを制限
async def get_message_info_cached(ctx, m):
    return await get_message_info(ctx, m)

@lru_cache(maxsize=256)
async def get_message_data(bot, m):
    try:
        print(f"get_message1 {datetime.now()}")
        c = bot.get_channel(m.channel_id)
        print(f"get_message2 {datetime.now()}")
        message = await c.fetch_message(m.message_id)
        print(f"get_message3 {datetime.now()}")
        return message
    except:
        return None
        

async def get_message_info(ctx, message):
    try:

        text = ""
        
        if message.content:
            content = message.content
            if len(message.content) >= 30:
                content = content[:30] + "..."
            text += f"Text: {content}\n"

        if message.attachments:
            file_name = ", ".join([attachment.filename for attachment in message.attachments[:2]])
            if len(file_name) > 30:
                file_name = file_name[:30] + "..."
            text += f"File: {file_name}\n"

        author_name = message.author.nick or message.author.global_name

        subtext = f"From: {author_name} ({message.author.name})\n"

        time = message.created_at + timedelta(hours=9)
        time = time.strftime('%Y-%m-%d %H:%M')
        subtext += f"When: {time}\n"

        subtext += f"https://discord.com/channels/{ctx.guild.id}/{message.channel.id}/{message.id}"

        return text,subtext

    except Exception as error:
        print(error)
        return "メッセージは消去されています",""  
    
async def pin(ctx, url, bot):
    try:
        await component_def.defer(ctx)
        print(ctx.data)
        res = url.split('/')

        user_id, guild_id = await component_def.return_user_data(ctx)

        if int(guild_id) != int(res[len(res)-3]):
            text = "このサーバーのメッセージではありません。\nメッセージのあるサーバーで操作を行ってください。"
            await component_def.followup_send_ephemeral(ctx, text)
            return
        
        c = bot.get_channel(int(res[len(res)-2]))
        p = await c.fetch_message(res[len(res)-1])
        print(p)
            
        pin_exist = await crud_pin.exist_pin(user_id, p.id, p.channel.id , p.guild.id)
        if pin_exist is True:   
            text = "既にピン留めされています"
            await component_def.followup_send_ephemeral(ctx, text)
            return
        
        user_id, message_id, channel_id, guild_id, add_time, exist = \
            user_id, p.id, p.channel.id, p.guild.id, datetime.now(), True

        await crud_pin.add_pin(user_id, message_id, channel_id, guild_id, add_time, exist)

        text = "URLのメッセージをピン留めしました。"
        await component_def.followup_send_ephemeral(ctx, text)       
        
    except Exception as e:
        print(e)

        text = "ピン留めに失敗しました"
        await component_def.followup_send_ephemeral(ctx, text)
    
async def pin_check(ctx, bot):
    try:

        user_id, guild_id = await component_def.return_user_data(ctx)

        if await crud_pin.check_user_id(user_id) is False:
            text = "ピン留めされたメッセージはありません"
            await component_def.message_response_ephemeral(ctx, text)
            return
        
        await component_def.defer(ctx)

        pinned_message = await crud_pin.fetch_pin(user_id, guild_id)
        print(datetime.now())

        pin_count = int(os.getenv("PIN_COUNT"))

        message = [get_message_data(bot, m) for m in pinned_message[0:pin_count]]
        messages = await asyncio.gather(*message)

        tasks = [get_message_info_cached(ctx, m) for m in messages]
        results = await asyncio.gather(*tasks)

        print(datetime.now())

        # embed にフィールドを追加する
        embed = discord.Embed(title="ピン留め一覧", description="")
        start = 0
        end = len(pinned_message) - 1

        print(datetime.now())

        for i, (text, subtext) in enumerate(results):
            embed.add_field(name=f"----------------\n{i+1}.\n{text}", value=f"{subtext}", inline=False)

            # 文字数が1500を超えたら、end を設定してループを抜ける
            if i == pin_count - 1:
                end = i
                break
        
        view = button_pin.pin_View(bot,user_id,start,end,pinned_message)
            
        print(datetime.now())
        await ctx.followup.send(embed=embed,view=view,ephemeral=True)

    except Exception as error:
        print(f"Error:{error}")


async def pin_menu(ctx, message):
    try:
        await component_def.defer(ctx)
        print(ctx.data)

        user_id, guild_id = await component_def.return_user_data(ctx)
            
        pin_exist = await crud_pin.exist_pin(user_id, message.id, message.channel.id , message.guild.id)
        if pin_exist is True:   
            text = "既にピン留めされています"
            await component_def.followup_send_ephemeral(ctx, text)
            return
        
        user_id, message_id, channel_id, guild_id, add_time, exist = \
            user_id, message.id, message.channel.id, message.guild.id, datetime.now(), True

        await crud_pin.add_pin(user_id, message_id, channel_id, guild_id, add_time, exist)

        text = "URLのメッセージをピン留めしました。"
        await component_def.followup_send_ephemeral(ctx, text)       
        
    except Exception as e:
        print(e)

        text = "ピン留めに失敗しました"
        await component_def.followup_send_ephemeral(ctx, text)