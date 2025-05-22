
import discord, os, asyncio
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

async def defer(ctx):
    await ctx.response.defer(ephemeral=True,thinking=True)

@lru_cache(maxsize=128)  # キャッシュサイズを制限
async def get_message_info_cached(ctx, m):
    return await get_message_info(ctx, m)

@lru_cache(maxsize=256)
async def get_message_data(ctx, m, bot):
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

    except Exception as e:
        print(e)
        return "メッセージは消去されています",""


class pin_View(discord.ui.View):
    def __init__(self, bot, player_id, start, end, pinned_message): # Viewにはtimeoutがあり、初期値は180(s)である
        super().__init__(timeout=600)
        self.player_id = player_id
        self.start = start
        self.end = end
        self.pinned_message = pinned_message

        print(len(pinned_message),pinned_message,end)

        if start != 0:
            self.add_item(BackPin(label="戻る",bot=bot,player_id=player_id,start=start,end=end,pinned_message=pinned_message))
        if end != len(pinned_message) - 1:
            self.add_item(GoPin(label="進む",bot=bot,player_id=player_id,start=start,end=end,pinned_message=pinned_message))

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)


class GoPin(discord.ui.Button):
    try:
        def __init__(self,bot,label,player_id,start,end,pinned_message):
            super().__init__(style=discord.ButtonStyle.primary, label=label)
            self.bot = bot
            self.player_id = player_id
            self.start = start
            self.end = end
            self.pinned_message = pinned_message
            print(self.start,self.end)

        async def callback(self, interaction: discord.Interaction):
            await defer(interaction)
            try:
                start = self.end + 1
                end = len(self.pinned_message)

                pin_count = int(os.getenv("PIN_COUNT"))

                embed = discord.Embed(title="ピン留め一覧",description="")

                message = [get_message_data(interaction, m,self.bot) for m in self.pinned_message[start:start+pin_count]]
                messages = await asyncio.gather(*message)

                tasks = [get_message_info_cached(interaction, msg) for msg in messages]
                results = await asyncio.gather(*tasks)

                for i, (text, subtext) in enumerate(results, start=start):
                    embed.add_field(name=f"--------------------\n{i+1}.\n{text}", value=f"{subtext}", inline=False)
                    end = i
                    if i == pin_count - 1:
                        break

                view = pin_View(self.bot,interaction.user.id,start,end,self.pinned_message)

                await interaction.edit_original_response(embed=embed,view=view)

            except AttributeError as e:
                await print(f"Error:{e}")
    except AttributeError as e:
        print(e)


class BackPin(discord.ui.Button):
    def __init__(self,bot,label,player_id,start,end,pinned_message):
            super().__init__(style=discord.ButtonStyle.primary, label=label)
            self.bot = bot
            self.player_id = player_id
            self.start = start
            self.end = end
            self.pinned_message = pinned_message
            print(self.start,self.end)

    async def callback(self, interaction: discord.Interaction):
        await defer(interaction)
        try:
            self.end = self.start
            end = self.end
            start = 0
            embed = discord.Embed(title="ピン留め一覧", description="")

            # 逆順の範囲を設定し、非同期タスクとしてメッセージをまとめて取得

            pin_count = int(os.getenv("PIN_COUNT"))
            
            message = [get_message_data(interaction, m,self.bot) for m in self.pinned_message[end-pin_count:end]]
            messages = await asyncio.gather(*message)

            tasks = [get_message_info_cached(interaction, msg) for msg in messages]
            results = await asyncio.gather(*tasks)

            # 結果を embed に追加
            for i, (text, subtext) in enumerate(results, start=start):
                embed.add_field(name=f"--------------------\n{end-pin_count+1+i}.\n{text}", value=f"{subtext}", inline=False)

                start = end - i - 1
                
                # embed の文字数が上限を超えた場合はループを抜ける
                if i == pin_count - 1:
                    break
            
            view = pin_View(self.bot,interaction.user.id,start,end-1,self.pinned_message)

            await interaction.edit_original_response(embed=embed,view=view)

        except AttributeError as e:
            await print(f"Error:{e}")