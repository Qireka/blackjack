import random


class Card(object):
    """一张牌"""

    def __init__(self, suite, face):
        self._face = face
        self._suite = suite

    @property
    def face(self):
        return self._face

    def __str__(self):
        return '%s%s' % (self._suite, self._face)


all_cards = [Card(suite, face)
             for suite in '♠♥♣♦'
             for face in list(range(2, 14)) + ['A', 'J', 'Q', 'K']]


class Poker(object):
    """一副牌"""

    def __init__(self):
        self._cards = [Card(suite, face)
                       for suite in '♠♥♣♦'
                       for face in list(range(2, 11)) + ['A', 'J', 'Q', 'K']]
        self._current = 0

    @property
    def cards(self):
        """显示牌"""
        return self._cards

    def shuffle(self):
        """洗牌"""
        self._current = 0
        random.shuffle(self._cards)

    @property
    def next(self):
        """发牌"""
        card = self._cards[self._current]
        self._current += 1
        return card

    @property
    def has_next(self):
        """还有没有牌
        与card长度比较
        还有牌返回Ture，否则返回False"""
        return self._current < len(self._cards)


class Player(object):
    """玩家"""

    def __init__(self):
        self._cards_on_hand = []
        self._point = 0
        self._is_alive = True

    @property
    def name(self):
        return self.name

    @property
    def cards_on_hand(self):
        return self._cards_on_hand

    @property
    def point(self):
        return self._point

    @property
    def is_alive(self):
        return self._is_alive

    @property
    def str_cards_on_hand(self):
        card_list = [str(i) for i in self.cards_on_hand]
        return ' '.join(card_list)

    def point_count(self):
        # 计算牌的点数
        self._point = 0
        has_ace = False
        for k in self.cards_on_hand:
            if k.face == 'J' or k.face == 'Q' or k.face == 'K':
                k_count = 10
            elif k.face == 'A':
                k_count = 1
            else:
                k_count = int(k.face)
            self._point += k_count
        for i in self._cards_on_hand:
            if i.face == 'A':
                has_ace = True
                break
            else:
                continue
        if has_ace is True:
            if self._point + 10 <= 21:
                self._point = self._point + 10
        if self.point > 21:
            self._is_alive = False
        return self._point

    def get(self, card):
        """摸牌"""
        self._cards_on_hand.append(card)
        self.point_count()

    def arrange(self, card):
        """理牌"""
        self._cards_on_hand.sort(key=card.face)


def main():
    p = Poker()
    p.shuffle()
    dealer = Player()
    player = Player()
    # 发牌
    dealer.get(p.next)
    dealer.get(p.next)
    player.get(p.next)
    player.get(p.next)
    print('庄家展示的明牌： %s' % dealer.cards_on_hand[0])
    print('玩家手牌： %s' % player.str_cards_on_hand)
    """
    if dealer.cards_on_hand[1].face == 'A':
        while True:
            insurance = input('是否买保险(y/n)')
            if insurance == 'y':
                # 赌注加一半
                if dealer.cards_on_hand[0].face == '10' or 'J' or 'Q' or 'K':
                    print('庄家另一张牌为%s' % dealer.cards_on_hand[0])
                    # 玩家赚一倍钱但是输掉赌注，游戏结束
                    break
                else:
                    break
            elif insurance == 'n':
                break
            else:
                print('输入错误')
            """

    # 玩家操作：
    can_double = True
    while True:
        if can_double:
            choice = input('请选择操作：\n 摸牌(H) 双倍(D) 停牌(S) \n')
        else:
            choice = input('请选择操作：\n 摸牌(H) 停牌(S) \n')
        # 摸牌
        if choice == 'H':
            player.get(p.next)
            print('抽了一张%s，当前手牌\n %s' % (player.cards_on_hand[-1], player.str_cards_on_hand))
        elif choice == 'D':
            # 双倍
            player.get(p.next)
            print('抽了一张%s，当前手牌\n %s' % (player.cards_on_hand[-1], player.str_cards_on_hand))
            break
        elif choice == 'S':
            print('玩家停牌')
            break
        else:
            print('输入错误')
        can_double = False
        if player.is_alive is False:
            break

    if player.is_alive:
        # 庄家操作
        print('庄家翻开暗牌：%s ，当前手牌 %s' % (dealer.cards_on_hand[1], dealer.str_cards_on_hand))
        while dealer.point < 17:
            dealer.get(p.next)
            print('抽了一张%s，当前手牌\n %s' % (dealer.cards_on_hand[-1], dealer.str_cards_on_hand))
        if dealer.is_alive:
            print('当前总点数：\n 庄家：%s \n 玩家：%s' % (dealer.point_count(), player.point_count()))
            if dealer.point_count() > player.point_count():
                print('庄家点数高于玩家，庄家获胜')
            elif dealer.point_count() < player.point_count():
                print('玩家点数高于庄家，玩家获胜')
            else:
                print('点数相同，平局')
        else:
            print('庄家爆了，玩家获胜')
    else:
        print('玩家爆了，庄家获胜')


if __name__ == '__main__':
    main()
