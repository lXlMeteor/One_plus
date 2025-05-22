#(会議用)タイムスタンプ機能

from datetime import datetime

import Component.component_def as component_def

async def startstamp(ctx):

    dt = datetime.now()
    dt = dt.strftime('%Y/%m/%d %H:%M:%S')

    text = f"会議を開始します。開始時刻は{dt}です。"

    await component_def.message_response(ctx, text)

async def endstamp(ctx):

    dt = datetime.now()
    dt = dt.strftime('%Y/%m/%d %H:%M:%S')

    text = f"会議を終了します。終了時刻は{dt}です。"
    
    await component_def.message_response(ctx, text)