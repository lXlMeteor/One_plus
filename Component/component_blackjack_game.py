#ブラックジャック(アルゴリズム)

import random

def card_get():
    return random.randint(1, 13)

def score_cal(s_list):
    s_list.sort(reverse=True)
    score = 0
    for s in s_list:
        if 2 <= s and s <= 9:
            score += s
        elif s >= 10:
            score += 10
        elif s == 1:
            if score + 11 > 21:
                score += 1
            else:
                score += 11
    return score

def dealer_score_cal(s_list):
    s_list.sort(reverse=True)
    score = 0
    for s in s_list:
        if 2 <= s and s <= 9:
            score += s
        elif s >= 10:
            score += 10
        elif s == 1:
            if score + 11 >= 17:
                score += 1
            else:
                score += 11
    return score

def score_check(score):
    if score > 21:
        return False
    else:
        return True

def dealer_check(score):
    if score < 17:
        return False
    else:
        return True

def blackjack():
    admin = []
    challenger = []
    
    # 最初のカード引き
    challenger_card = card_get()
    admin_card = card_get()
    
    challenger.append(challenger_card)
    admin.append(admin_card)
    
    return admin, challenger  # 初期状態を返す

def draw_card(challenger):
    challenger_card = card_get()
    challenger.append(challenger_card)
    return challenger_card, challenger  # 引いたカードと新しい手札を返す

def dealer_turn(admin):
    admin_card = card_get()
    admin.append(admin_card)
    return admin_card, admin
