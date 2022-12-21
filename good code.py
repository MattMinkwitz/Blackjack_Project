import random

def get_num(message, min, max):
    """
    The function get_num is a global variable that is utilized to print a message to a player followed by an integer
    value between the min and max parameters.
    """
    value = str(min - 1)
    while (not value.isnumeric()) and (min >= int(value) or int(value) >= max):
        value = input(message)
    return int(value)


def get_float(message, min, max):
    """
    The function get_float is a global variable that is utilized to print a message to a player followed by a
    float value between the min and max parameters.
    """
    value = str(min - 1)
    while (not value.isnumeric()) and (min >= float(value) or float(value) >= max):
        value = input(message)
    return float(value)


class BlackJack(object):
    """
    A data type for in game BlackJack Play
    """

    def __init__(self):
        """
        constructor for in game BlackJack objects
        """
        self.limit = 22
        self.dealer = Dealer(self.limit)
        self.deck = CardDeck()
        self.players = [self.dealer]

    def sit_at_table(self):
        """
        The function sit_at_table uses human_player = Player(self.limit, "you", 1000)
        and self.add_player(human_player) to create a human_player and adds the player to the BlackJack game with a card
        limit set at 22 and points set at 1000. As long as the player has more than 0 points a player can choose from
        the menu items to either begin game, create another player, delete a player, or quit the game.If a player
        chooses an option other the 1-4 the input will not be understood.
        """
        human_player = Player(self.limit, "you", 1000)
        self.add_player(human_player)
        while True:
            if human_player.points <= 0:
                print("You lose")
                return
            print("1) begin game \n2) add players \n3) remove players \n4) quit")
            player_input = input("Enter choice ")

            match player_input:
                case "1":
                    self.begin_game(human_player)
                case "2":
                    self.create_player_menu(self.limit)
                case "3":
                    self.delete_player_menu()
                case "4":
                    break
                case _:
                    print("input not understood")

    def add_player(self, player):
        """
        The function add_player uses insert() to add a player to the game at the given list index
        """
        self.players.insert(0, player)

    def begin_game(self, human_player):
        """
        The function begin_game starts a new game of BlackJack, first by resetting the deck of cards to its original
        amount of 52 and then randomly shuffling the deck of 52 cards. for a player inserted in self.players if a player
        has over 0 points they will be asked how much they would like to Ante, if a player has no points they leave
        the table and will be removed from the game. ph represents a players hand, by calling
        ph.rec_card(self.deck.deal_card()) twice will deal a player two cards. if a player has cards totaling 21
        player.hand.is_natrual() is called and the player will receive there ante back + the dealers match of their ante
        if there are no other players added to the game player.wins() is called and the round will be over followed by
        player.hand.drop() to clear their hand and num_turn increments by 1.
        However if a player has under 21 points they can either choose to stand with their hand or not stand and
        recive another card. If that makes a player go over 21 player.hand.is_bust() is called and they lose the round.
        Finally if the player and dealer are not is_bust() and if self.dealer.hand.sum() greater than player.hand.sum()
        the player loses. in both cases' player.loses() is called and the player pays their ante to the dealer,
        their cards are cleared, and num_turn incremented by 1.
        """

        num_turn = 0

        self.deck.reset()
        self.deck.shuffle()

        for player in self.players:
            ante = player.get_ante()

            if ante <= 0:
                print(f"player {player.name} leaves table")
                self.players.remove(player)
                continue
            ph = player.hand
            ph.rec_card(self.deck.deal_card())
            ph.rec_card(self.deck.deal_card())
        for player in self.players:
            num_turn += 1
            ph = player.hand
            if not player == human_player:
                print(player)
            while not player.stands(self.deck):
                card = self.deck.deal_card()
                print(f"dealer has delt card: {card}")
                ph.rec_card(card)
                if not player == human_player:
                    print(player)
                if ph.is_bust() or ph.is_natrual():
                    break
            if ph.is_bust():
                print(f"player: {player.name} went over limit")
        for player in self.players:
            if player == self.dealer:
                self.dealer.hand.drop()
                continue
            if player.hand.is_bust():
                player.loses()
            else:
                if self.dealer.hand.is_bust():
                    player.wins()
                    self.dealer.loses()
                elif self.dealer.hand.sum() < player.hand.sum():
                    player.wins()
                    self.dealer.loses()
                elif self.dealer.hand.sum() > player.hand.sum():
                    player.loses()
                    self.dealer.wins()
                else:
                    player.tie()
            player.hand.drop()

    def create_player_menu(self, limit):
        """
        The function create_player_menu allows a person to add an AIPlayer to the game. After entering a name.
        The player will then be allowed to choose how many points to start with up to the max which is set at 1000.
        Lastly a player will be able to select the AIPlayers risk from 0-1
        if their evaluated_risk is less than their risk of choice the AIPlayer will receive another card.
        """
        new_player_name = input("What is your name?")
        new_player_points = get_num("How many points, -1 for infinite, otherwise maximum 1000", -2, 1000)
        new_player_risk = get_float("what is their risk 0-1", 0, 1)

        new_player = AIPlayer(limit, int(new_player_risk), new_player_name, int(new_player_points))
        self.add_player(new_player)

    def delete_player_menu(self):
        """
        The function delete_player_name allows a user to delete an AIPlayer they created. if they choose "you" or
        the "dealer" they will not be allowed to do so because one cannot delete themselves or the dealer.
        If they choose anyone but the "dealer" and "you" the player in self.players will be removed from the game.
        """
        delete_player_name = input("What is your name?")
        if delete_player_name == "you":
            print("you can't delete yourself")
            return
        if delete_player_name == "dealer":
            print("you can't delete dealer")
            return
        for player in self.players:
            if player.name == delete_player_name:
                self.players.remove(player)


class Card(object):
    """
    A data type for BlackJack Card
    """

    def __init__(self, suit, card_type, card_vals):
        """
        Constructor for Blackjack Card objects.
        """
        self.suit = suit
        self.card_vals = card_vals
        self.card_type = card_type

    def __repr__(self):
        """
        returns a string representation of the card_type of the cards suit
        """
        return self.card_type + ", of " + self.suit

    def low_val(self):
        """
        The function low_val returns an ace value of 1
        it also is a useful function to figure out how many cards are under the limit and how many cards are over
        for the AIPlayers risk evaluation
        """
        return self.card_vals[0]

    def high_val(self):
        """
        returns an ace value of 11
        """
        return self.card_vals[-1]


class CardDeck(object):
    """
    Data type for a Blackjack CardDeck
    """

    def __init__(self):
        """
        constructor for CardDeck objects
        """
        self.cards = []
        self.dealt_cards = []
        self.suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
        self.card_types = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen',
                           'King', 'Ace')
        self.vals = {'Two': [2], 'Three': [3], 'Four': [4], 'Five': [5], 'Six': [6], 'Seven': [7], 'Eight': [8],
                     'Nine': [9], 'Ten': [10], 'Jack': [10], 'Queen': [10], 'King': [10], 'Ace': [1, 11]}

        self.reset()

    def size(self):
        """
        The function size will return how many cards are in the deck
        """
        return len(self.cards)

    def reset(self):
        """
        The function reset creates a list of 52 cards for the deck by appending it to the empty list "cards"
        and by calling reset() it allows the deck to be refilled with the 52 cards
        """
        self.cards = []
        self.dealt_cards = []
        for s in self.suits:
            for c in self.card_types:
                self.cards.append(Card(s, c, self.vals[c]))

    def shuffle(self):
        """
        The function shuffle randomly shuffles the CardDeck
        """
        random.shuffle(self.cards)

    def deal_card(self):
        """
        The function deal_card uses the pop function to remove the card item from the deck of cards and deals it to the
        player. It also keeps track of the cards given out by appending the removed card to delt_cards
        (useful for AIPlayer risk evaluation)
        """
        # pop() function will remove last card in the deck
        one_card = self.cards.pop()
        self.dealt_cards.append(one_card)
        return one_card

    def num_cards_over(self, n):
        """
        The function num_cards_over utilizes the low_val() function to see how many cards are left in the deck
        that will make a player go over the limit
        (useful for AIPlayer risk evaluation)
        """
        count = 0
        for card in self.cards:
            if card.low_val() > n:
                count += 1
        return count

    def num_cards_under(self, n):
        """
        The function num_cards_under utilizes the low_val() function to see how many cards are left in the deck
        that will make a player stay under the limit
        (useful for AIPlayer risk evaluation)
        """
        count = 0
        for card in self.cards:
            if card.low_val() < n:
                count += 1
        return count


class Player(object):
    """
    data type for a Blackjack Player
    """
    def __init__(self, limit, name, points):
        """constructor for Player objects """
        self.name = name
        self.points = points
        self.hand = PlayerHand(limit)

    def __repr__(self):
        """
        returns a string representation of a players name and points plus the players current hand
        """
        return f"name: {self.name} -- points: {self.points}" + ("" if (len(self.hand.cards) == 0) else f"\n{self.hand}")

    def stands(self, deck):
        """
        The function stands
        Returns False to stand for responses of "yes" "ye" "y" and the player will receive another card.
        Returns True to stand for responses of "no" or "n" and a player will not receive another card.
        """
        response = ""
        print(self.__repr__())
        while response == "":
            response = input("Do you want a card (yes/no)").lower()
            match response:
                case "yes":
                    return False
                case "ye":
                    return False
                case "y":
                    return False
                case "no":
                    return True
                case "n":
                    return True
                case _:
                    print("input no understood")
                    response = ""

    def get_ante(self):
        """
        The function get_ante allows a player to select how many points they would like to ante at the start of a new
        round and returns their choice of ante.
        """
        while self.hand.ante <= 0:
            print(self)
            self.hand.ante = get_num(f"How much do you want to ante 1-{self.points}", 0, self.points + 1)
        return self.hand.ante

    def wins(self):
        """
        The function wins adds the players original ante + the dealers match of their ante back into their points
        """
        self.points += self.hand.ante
        print(f"player: {self.name} wins, points: {self.points}")

    def loses(self):
        """
         The function loses takes the players ante and subtracts it from their points
        """
        self.points -= self.hand.ante
        print(f"player: {self.name} lose, points: {self.points}")

    def tie(self):
        self.points = self.points
        print(f"player: {self.name} tie, points: {self.points}")


class AIPlayer(Player):
    """
    AIPlayer is a child class for the Player class
    """
    def __init__(self, limit, risk, name, points):
        """
        constructor to inherit limit, name, and points from Player class and also initializes risk
        """
        self.risk = risk
        super().__init__(limit, name, points)

    def stands(self, deck):
        """
        The function stands overrides the original stands from Player. it calculates how far until the AIPlayer goes
        over the limit and makes an evaluated risk based upon the num_cards_over (number of cards over the limit in what
        is left in the deck). When a player creates their player and chooses the risk from the AIPlayer if the evaluated
        risk is less than their risk of choice the AIPlayer receives another card. otherwise, the AIPlayer will stand.
        """
        distance = self.hand.limit - self.hand.sum()
        evaluated_risk = deck.num_cards_over(distance) / deck.size()
        if evaluated_risk < self.risk:
            return False
        else:
            print(f"player {self.name} stands")
            return True

    def get_ante(self):
        """
        The function get_ante overrides Players get_ante, by getting a new_ante from 10% of their limit
        if the new ante is less than 0 it returns 1 otherwise will return the new_ante
        """
        new_ante = self.hand.ante * .1
        if new_ante <= 0:
            return 1
        else:
            return new_ante


class Dealer(AIPlayer):
    """
    the class Dealer is a child class of AIPlayer
    """
    def __init__(self, limit):
        """
        Inherits limit from AIPlayer, sets dealers risk at .8, creates their name "dealer", and using -1 gives them
        unlimited points
        """
        super().__init__(limit, 0.8, "dealer", -1)

    def stands(self, deck):
        """
        The function stands overrides AIPlayers stands function to implement the rule that a dealer cannot choose to
        receive another card if their hand totals 17 or greater. if their hand is less than 17
        super().stands is called to use the risk evaluation for the dealer to either stand or get another card
        """
        if self.hand.sum() >= 17:
            return True
        else:
            super().stands(deck)


class PlayerHand(object):
    """
    data type for Blackjack PlayersHand
    """

    def __init__(self, limit):
        """
        A constructor for PlayerHand objects
        """
        self.cards = []
        self.limit = limit
        self.ante = 0

    def rec_card(self, card):
        """
        The function rec_card Allows a player to receive another card and sorts for high to low values
        """
        self.cards.append(card)
        self.cards.sort(reverse=True, key=self.card_sort)

    def sum(self):
        """
        The function sum returns the sum of card values for a PlayersHand
        if using the high val for the ace (11) is under the limit an ace val of 11 will be added to the sum.
        else the low val (1) will be added to the sum
        """
        sum = 0
        for c in self.cards:
            if sum + c.high_val() < self.limit:
                sum += c.high_val()
            else:
                sum += c.low_val()
        return sum

    def is_bust(self):
        """
        The function is_bust returns True if a Players hand is over the limit
        """
        return self.sum() >= self.limit

    def is_natrual(self):
        """
        The function is_natrual returns True is a PlayersHand is = to 21
        """
        return self.sum() == self.limit - 1

    def card_sort(self, card):
        """
        The function card_sort sorts the PlayersHand by the low val
        """
        return card.low_val()

    def drop(self):
        """
        the function drop clears the players in the games deck once the round is over and resets their ante back to 0
        """
        self.cards.clear()
        self.ante = 0

    def __repr__(self):
        """
        returns a string representation of ante, players cards and the sum of the hand
        """
        s = "ante: " + str(self.ante) + "\n"
        for c in self.cards:
            s += '[' + c.__repr__() + "], "
        s = s[0:-2]
        s += ": " + str(self.sum())
        return s


Game = BlackJack()
Game.sit_at_table()
