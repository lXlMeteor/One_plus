import requests
import time

# 実行するコード（Python3）
code = '''
print("Hello from paiza.io!")
'''

# ステップ1: コードを送信してジョブを作成
create_url = "https://api.paiza.io:443/runners/create"
params = {
    "source_code": code,
    "language": "python3",
    "api_key": "guest"  # 公開APIキー
}

response = requests.post(create_url, json=params)
result = response.json()
id = result.get("id")

if not id:
    print("ジョブの作成に失敗しました。")
    print(result)
else:
    # ステップ2: 結果取得（非同期なので少し待つ）
    get_url = "https://api.paiza.io:443/runners/get_details"
    while True:
        time.sleep(1)
        res = requests.get(get_url, params={"id": id, "api_key": "guest"})
        details = res.json()
        if details.get("status") == "completed":
            print("出力結果:")
            print(details.get("stdout"))
            print("エラー出力:")
            print(details.get("stderr"))
            break
        else:
            print("まだ実行中です...")
