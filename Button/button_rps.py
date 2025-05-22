
import discord, random


class RPSView(discord.ui.View):
    def __init__(self, player_id):
        super().__init__(timeout=180)  # タイムアウトを設定

        self.add_item(JankenButton("グー", player_id))
        self.add_item(JankenButton("チョキ", player_id))
        self.add_item(JankenButton("パー", player_id))


class JankenButton(discord.ui.Button):
    def __init__(self, label, player_id):
        super().__init__(style=discord.ButtonStyle.primary, label=label)
        self.player_id = player_id

    async def callback(self, interaction: discord.Interaction):

        if interaction.user.id != self.player_id:
            await interaction.response.send_message("このゲームには参加できません。", ephemeral=True)
            return
        
        user_hand = self.label
        bot_hand = random.choice(["グー","チョキ","パー"])
        
        # 勝敗判定
        if user_hand == bot_hand:
            result = "引き分け！"
        elif (user_hand == "グー" and bot_hand == "チョキ") or \
             (user_hand == "チョキ" and bot_hand == "パー") or \
             (user_hand == "パー" and bot_hand == "グー"):
            result = "あなたの勝ち！"
        else:
            result = "あなたの負け..."
        
        # 結果を送信
        await interaction.response.edit_message(content=f"あなた: {user_hand}\nボット: {bot_hand}\n結果: {result}", view=None)
