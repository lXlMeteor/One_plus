
import discord, math

import Component.component_blackjack_game as compose_blackjack_game
import Database.crud_blackjack as crud_blackjack

games = {}

def card_change(card):

    if card == 11:
        card = 'J'
    elif card == 12:
        card = 'Q'
    elif card == 13:
        card = 'K'
    elif card == 1:
        card = 'A'

    return card


class BlackjackView(discord.ui.View):
    def __init__(self, player_id, admin,challenger):
        super().__init__(timeout=180)  # タイムアウトを設定

        #まだ辞書型にしているので、変更する必要あり
        self.player_id = player_id
        games[player_id] = {'admin': admin, 'challenger': challenger}

    @discord.ui.button(label="ヒット", style=discord.ButtonStyle.primary)
    async def hit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.player_id:
            await interaction.response.send_message("このゲームには参加できません。", ephemeral=True)
            return
        
        game = games[self.player_id]
        challenger_card, game['challenger'] = compose_blackjack_game.draw_card(game['challenger'])
        challenger_score = compose_blackjack_game.score_cal(game['challenger'])

        challenger_card = card_change(challenger_card)
        admin_card = card_change(game['admin'][0])

        if compose_blackjack_game.score_check(challenger_score) is False:
            await interaction.response.edit_message(content=f"あなたは {challenger_card} を引きました。現在のスコア: {challenger_score}\nあなたのスコアが21を超えました。あなたの負けです。", view=None)
            del games[self.player_id]
        else:
            await interaction.response.edit_message(content=f"あなたは {challenger_card} を引きました。\n現在のスコア: {challenger_score}\nディーラーの最初のカードは{admin_card}です。")

    @discord.ui.button(label="スタンド", style=discord.ButtonStyle.secondary)
    async def stand_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.player_id:
            await interaction.response.send_message("このゲームには参加できません。", ephemeral=True)
            return

        game = games[self.player_id]
        
        admin_card,game['admin'] = compose_blackjack_game.dealer_turn(game['admin'])
        admin_card = card_change(admin_card)

        text = ""

        text += f"ディーラーのカードは{card_change(game['admin'][0])}、{admin_card}でした。\n"

        admin_score = compose_blackjack_game.dealer_score_cal(game['admin'])

        text += f"ディーラーはスコア{admin_score}からカードを引きます\n"

        # ディーラーのターン処理
        while admin_score < 17:
            admin_card, game['admin'] = compose_blackjack_game.dealer_turn(game['admin'])

            card = card_change(admin_card)
            text += f"ディーラーは{card}を引きました\n"
            admin_score = compose_blackjack_game.dealer_score_cal(game['admin'])

        challenger_score = compose_blackjack_game.score_cal(game['challenger'])

        result = ""
        if challenger_score > 21:
            result = "あなたのスコアは21を超えたのであなたの負けです。"
        elif admin_score > 21:
            result = "ディーラーのスコアが21を超えたのであなたの勝ちです。"
        elif challenger_score > admin_score:
            result = "あなたの勝ちです。"
        elif challenger_score == admin_score:
            result = "引き分けです。"
        else:
            result = "あなたの負けです。"

        # 最終結果を表示し、ゲームを終了
        await interaction.response.edit_message(content=f"{text}\n最終結果\nあなたのスコア：{challenger_score}\nディーラーのスコア：{admin_score}\n{result}", view=None)
        del games[self.player_id]

class Coin_BlackjackView(discord.ui.View):
    def __init__(self, player_id, admin,challenger,guild_id,coin):
        super().__init__(timeout=180)  # タイムアウトを設定

        #まだ辞書型にしているので、変更する必要あり
        self.player_id = player_id
        self.guild_id = guild_id
        self.coin = coin
        games[player_id] = {'admin': admin, 'challenger': challenger}

    @discord.ui.button(label="ヒット", style=discord.ButtonStyle.primary)
    async def hit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.player_id:
            await interaction.response.send_message("このゲームには参加できません。", ephemeral=True)
            return
        
        game = games[self.player_id]
        challenger_card, game['challenger'] = compose_blackjack_game.draw_card(game['challenger'])
        challenger_score = compose_blackjack_game.score_cal(game['challenger'])

        challenger_card = card_change(challenger_card)
        admin_card = card_change(game['admin'][0])

        if compose_blackjack_game.score_check(challenger_score) is False:
            credit = await crud_blackjack.coin_add(self.player_id, self.guild_id, self.coin*-1)
            await interaction.response.edit_message(content=f"あなたは {challenger_card} を引きました。現在のスコア: {challenger_score}\nあなたのスコアが21を超えました。あなたの負けです。\n\n残りのコイン数：{credit}", view=None)
            del games[self.player_id]
        else:
            await interaction.response.edit_message(content=f"あなたは {challenger_card} を引きました。\n現在のスコア: {challenger_score}\nディーラーの最初のカードは{admin_card}です。")

    @discord.ui.button(label="スタンド", style=discord.ButtonStyle.secondary)
    async def stand_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.player_id:
            await interaction.response.send_message("このゲームには参加できません。", ephemeral=True)
            return

        game = games[self.player_id]

        admin_card,game['admin'] = compose_blackjack_game.dealer_turn(game['admin'])
        admin_card = card_change(admin_card)

        text = ""

        text += f"ディーラーのカードは{card_change(game['admin'][0])}、{admin_card}でした。\n"

        admin_score = compose_blackjack_game.score_cal(game['admin'])

        text += f"ディーラーはスコア{admin_score}からカードを引きます\n"

        # ディーラーのターン処理
        while admin_score < 17:
            admin_card, game['admin'] = compose_blackjack_game.dealer_turn(game['admin'])
            admin_card = card_change(admin_card)
            text += f"ディーラーは{admin_card}を引きました\n"
            admin_score = compose_blackjack_game.score_cal(game['admin'])

        challenger_score = compose_blackjack_game.score_cal(game['challenger'])

        result = ""

        if challenger_score == 21 and len(game['challenger']) == 2:
            result = "ブラックジャック！あなたの勝ちです。"
            credit = await crud_blackjack.coin_add(self.player_id, self.guild_id, math.floor(self.coin*1.5))
        elif challenger_score > 21:
            result = "あなたのスコアは21を超えたのであなたの負けです。"
            credit = await crud_blackjack.coin_add(self.player_id, self.guild_id, self.coin*-1)
        elif admin_score > 21:
            result = "ディーラーのスコアが21を超えたのであなたの勝ちです。"
            credit = await crud_blackjack.coin_add(self.player_id, self.guild_id, self.coin)
        elif challenger_score > admin_score:
            result = "あなたの勝ちです。"
            credit = await crud_blackjack.coin_add(self.player_id, self.guild_id, self.coin)
        elif challenger_score == admin_score:
            result = "引き分けです。"
            credit = await crud_blackjack.coin_add(self.player_id, self.guild_id, 0)
        else:
            result = "あなたの負けです。"
            credit = await crud_blackjack.coin_add(self.player_id, self.guild_id, self.coin*-1)


        # 最終結果を表示し、ゲームを終了
        await interaction.response.edit_message(content=f"{text}\n最終結果\nあなたのスコア：{challenger_score}\nディーラーのスコア：{admin_score}\n{result}\n\n残りのコイン数：{credit}", view=None)
        del games[self.player_id]