import random
import sys

def card_get():
    return random.randint(1,13)

def kaigyo():
    return print()

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

def main():
    blackjack()
    print("再戦しますか？")
    action = input("1.はい　2.いいえ：")
    if action == "1":
        main()
    else:
        sys.exit()


def blackjack():

    admin = []
    challenger = []
    admin_score = 0
    challenger_score = 0

    challenger_card = card_get()
    print(f"プレイヤーは{challenger_card}を引きました")
    challenger.append(challenger_card)
        

    admin_card = card_get()
    print(f"ディーラーは{admin_card}を引きました")
    admin.append(admin_card)

    kaigyo()

    while True:

        admin_score = score_cal(admin)
        challenger_score = score_cal(challenger)

        print(f"あなたのスコア：{challenger_score}")
        print(f"ディーラーのスコア：{admin_score}")
        kaigyo()
        print("あなたはどうしますか？")

        challenger_action = input("1,ヒット　2,スタンド：")
        if challenger_action == "1":
            challenger_card = card_get()
            kaigyo()
            print("ヒット！")
            print(f"プレイヤーは{challenger_card}を引きました")
            kaigyo()
            challenger.append(challenger_card)
        else:
            print("スタンド！")
            break

        challenger_score = score_cal(challenger)

        if score_check(challenger_score) is False:
            print(f"あなたのスコア：{challenger_score}")
            print("あなたのスコアが21を超えました")
            print("あなたの負けです")
            return
            

    while admin_score < 17:
        admin_card = card_get()
        print(f"ディーラーは{admin_card}を引きました")
        admin.append(admin_card)
        admin_score = score_cal(admin)
        print(f"ディーラーのスコア：{admin_score}")

        if dealer_check(admin_score) is True:
            break

    kaigyo()
    print("最終結果")
    print(f"あなたのスコア：{challenger_score}")
    print(f"ディーラーのスコア：{admin_score}")


    if challenger_score > 21:
        print("あなたのスコアは21を超えたのであなたの負けです")
    elif admin_score > 21:
        print("ディーラーのスコアが21を超えたのであなたの勝ちです")
    elif challenger_score > admin_score:
        print("あなたの勝ちです")
    elif challenger_score == admin_score:
        print("引き分けです")
    else:
        print("あなたの負けです")
            

main()


    


