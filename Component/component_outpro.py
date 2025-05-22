#オンラインプログラム実行機能

import discord, asyncio, os, requests, time
from functools import lru_cache
from dotenv import load_dotenv
import aiohttp

import Component.component_def as component_def

async def outpro(ctx, lang, input, file):

    await component_def.defer_n(ctx)

    print(lang)
    url = "https://api.paiza.io:443"
    language = lang.value
    file_bytes = await file.read()

# テキストとしてデコード（例：UTF-8）
    source = file_bytes.decode('utf-8')

    print(source)
    print(language)
    print(input)

    params = {
        'api_key':'guest',
        'source_code':source,
        'language':language,
        'input':input
    }
    print(params)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url + '/runners/create', json=params, timeout=10) as response:
                result = await response.json()

        print(result)
        id = result['id']

        time.sleep(1.0)

        params = {
            'id': id,
            'api_key':'guest'
        }

        response = requests.get(
            url + '/runners/get_details',
            json=params
        )

        result = response.json()
    

        print(result)

        text = ''

        await component_def.followup_send(ctx, f"{result['stdout']}, {result['stderr']}")
    
    except AttributeError as e:
        print(e)

