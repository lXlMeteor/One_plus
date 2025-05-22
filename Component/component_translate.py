#簡単翻訳機能

from googletrans import Translator
from langdetect import detect

import Component.component_def as component_def

# 言語コードと日本語名の対応表
language_code_map = {
  "is": "アイスランド語",
  "ay": "アイマラ語",
  "ga": "アイルランド語",
  "az": "アゼルバイジェン語",
  "as": "アッサム語",
  "aa": "アファル語",
  "ab": "アプハジア語",
  "af": "アフリカーンス語",
  "am": "アムハラ語",
  "ar": "アラビア語",
  "sq": "アルバニア語",
  "hy": "アルメニア語",
  "it": "イタリア語",
  "yi": "イディッシュ語",
  "iu": "イヌクティトット語",
  "ik": "イヌピア語",
  "ia": "インターリングア (国際語)",
  "ie": "インターリング語",
  "id": "インドネシア語",
  "ug": "ウイグル語",
  "cy": "ウェールズ語",
  "vo": "ヴォラピュック語",
  "wo": "ウォロフ語",
  "uk": "ウクライナ語",
  "uz": "ウズベク語",
  "ur": "ウルドゥー語",
  "en": "英語",
  "et": "エストニア語",
  "eo": "エスペラント語",
  "or": "オーリア語",
  "oc": "オキタン語",
  "nl": "オランダ語",
  "om": "オロモ語 (ガラ語)",
  "kk": "カザフ語",
  "ks": "カシミール語",
  "ca": "カタラン語",
  "gl": "ガリシア語",
  "ko": "韓国語",
  "kn": "カンナダ語",
  "km": "カンボジア語",
  "rw": "キヤーワンダ語 (ルアンダ語)",
  "el": "ギリシャ語",
  "ky": "キルギス語",
  "rn": "キルンディ語 (ルンディ語)",
  "gn": "グアラニー語",
  "qu": "クエチュア語",
  "gu": "グジャラト語",
  "kl": "グリーンランド語",
  "ku": "クルド語",
  "hr": "クロアチア語",
  "gd": "ゲーリック語 (スコットランド語)",
  "gv": "ゲーリック語 (マン島語)",
  "xh": "コーサ語",
  "co": "コルシカ語",
  "sm": "サモア語",
  "sg": "サングホ語",
  "sa": "サンスクリット語",
  "ss": "シスワティ語",
  "jv": "ジャワ語",
  "ka": "ジョージア語",
  "sn": "ショナ語",
  "sd": "シンド語",
  "si": "シンハラ語",
  "sv": "スウェーデン語",
  "su": "スーダン語",
  "zu": "ズールー語",
  "es": "スペイン語",
  "sk": "スロヴァキア語",
  "sl": "スロヴェニア語",
  "sw": "スワヒリ語 (キスワヒリ語)",
  "tn": "セツワナ語",
  "st": "セト語",
  "sr": "セルビア語",
  "sh": "セルボクロアチア語",
  "so": "ソマリ語",
  "th": "タイ語",
  "tl": "タガログ語",
  "tg": "タジク語",
  "tt": "タタール語",
  "ta": "タミル語",
  "cs": "チェコ語",
  "ti": "チグリニャ語",
  "bo": "チベット語",
  "zh-cn": "中国語 (簡体)",
  "zh-tw": "中国語 (繁体)",
  "ts": "ヅォンガ語",
  "te": "テルグ語",
  "da": "デンマーク語",
  "de": "ドイツ語",
  "tw": "トウィ語",
  "tk": "トルクメン語",
  "tr": "トルコ語",
  "to": "トンガ語",
  "na": "ナウル語",
  "ja": "日本語",
  "ne": "ネパール語",
  "no": "ノルウェー語",
  "ha": "ハウサ語",
  "be": "白ロシア語 (ベラルーシ語)",
  "ba": "バシキール語",
  "ps": "パシト語 (パシュトー語)",
  "eu": "バスク語",
  "hu": "ハンガリー語",
  "pa": "パンジャビ語",
  "bi": "ビスラマ語",
  "bh": "ビハール語",
  "my": "ビルマ語",
  "hi": "ヒンディー語",
  "fj": "フィジー語",
  "fi": "フィンランド語",
  "dz": "ブータン語",
  "fo": "フェロー語",
  "fr": "フランス語",
  "fy": "フリジア語",
  "bg": "ブルガリア語",
  "br": "ブルターニュ語",
  "vi": "ベトナム語",
  "he": "ヘブライ語",
  "fa": "ペルシャ語",
  "bn": "ベンガル語",
  "pl": "ポーランド語",
  "pt": "ポルトガル語",
  "mi": "マオリ語",
  "mk": "マカドニア語",
  "mg": "マダガスカル語",
  "mr": "マラッタ語",
  "ml": "マラヤーラム語",
  "mt": "マルタ語",
  "ms": "マレー語",
  "mo": "モルダビア語",
  "mn": "モンゴル語",
  "yo": "ヨルバ語",
  "lo": "ラオタ語",
  "la": "ラテン語",
  "lv": "ラトビア語 (レット語)",
  "lt": "リトアニア語",
  "ln": "リンガラ語",
  "li": "リンブルク語",
  "ro": "ルーマニア語",
  "rm": "レートロマンス語",
  "ru": "ロシア語"
}


# 言語コードを日本語名に変換する関数
def get_language_name_from_code(language_code):
    for key in language_code_map:
        if language_code in key:
            return language_code, language_code_map[language_code]

    return language_code_map.get(language_code, "未知の言語")


async def translate(ctx, message):

    await component_def.defer(ctx)

    translator = Translator()

    lang = detect(message.content)
    lang, lang_ja = get_language_name_from_code(lang)

    try:
        trans_text = translator.translate(message.content, src=f'{lang}', dest='ja')
        print(detect(message.content))

        text = f"**{lang_ja}の翻訳を行います。なお、翻訳精度は低いため参考程度にしてください。**"

        text += f"```{trans_text.text}```"
    
    except:

        text = "申し訳ありません。翻訳できませんでした。"
    
    finally:

        await component_def.followup_send_ephemeral(ctx, text)

