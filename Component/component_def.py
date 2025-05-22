#汎用関数(レスポンスなど)

async def message_response_ephemeral(ctx, text):
    await ctx.response.send_message(text,ephemeral=True)

async def return_user_data(ctx):
    user_id = ctx.user.id
    guild_id = ctx.guild.id

    return user_id, guild_id

async def message_response(ctx, text):
    await ctx.response.send_message(text)

async def followup_send_ephemeral(ctx, text):
    await ctx.followup.send(text,ephemeral=True)

async def followup_send(ctx, text):
    await ctx.followup.send(text,ephemeral=False)

async def defer(ctx):
    await ctx.response.defer(ephemeral=True,thinking=True)

async def defer_n(ctx):
    await ctx.response.defer(thinking=True)