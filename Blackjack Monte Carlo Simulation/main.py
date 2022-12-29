import random
from copy import deepcopy
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

# ----- Configuration Options -----
num_decks = 8
shuffle_percentage = .5  # Frequency of the shoe being reshuffled, re-integrating previously dealt cards
initial_bank = 100
initial_bet = 10
simulations = 1000  # Amount of total independent simulations

# ----- Creating a Shoe -----
std_deck = [
        # 2  3  4  5  6  7  8  9  10  J   Q   K   A
        2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
        2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
        2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
        2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
    ]

shoe = std_deck * num_decks
random.shuffle(shoe)

# ----- Initialization -----
dealt_cards = []
hand = []
score = 0
new_card = []
running_count = []
card_values = {}


class Deal:  # Handles all the dealing functions
    def __init__(self, hand, score, new_card, running_count, card_values):
        self.hand = hand
        self.score = score
        self.new_card = new_card
        self.running_count = running_count
        self.card_values = card_values

    def deal_initial_hand(self):  # deal the initial hand (2 cards)
        global dealt_cards
        need_reshuffle()
        self.hand = shoe.pop(0), shoe.pop(0)
        self.hand = list(self.hand)
        dealt_cards += self.hand
        self.compute_score()
        return self.ace_checker()

    def hit(self):  # deal an additional card
        global dealt_cards
        need_reshuffle()
        self.new_card = shoe.pop(0)
        self.hand.append(self.new_card)
        dealt_cards.append(self.new_card)
        self.compute_score()
        return self.ace_checker()

    def compute_score(self):  # compute the score of the hand
        self.score = sum(self.hand)
        high_low_player.score = self.score
        return self.score

    def ace_checker(self):  # check if aces should be converted from 11 to 1
        i = 0
        while i < len(self.hand):
            if self.score > 21 and self.hand[i] == 11:
                self.hand[i] = 1
                self.compute_score()
            i += 1
        return self.score


class Algorithms:
    # Beginner Card-Counting Algorithm card values
    high_low_card_values = {
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 1,
        7: 0,
        8: 0,
        9: 0,
        10: -1,
        11: -1
    }
    zen_count_card_values = {
        2: 1,
        3: 1,
        4: 2,
        5: 2,
        6: 2,
        7: 1,
        8: 0,
        9: 0,
        10: -2,
        11: -1
    }
    # Intermediate Card-Counting Algorithm card values
    omega_2_card_values = {
        2: 1,
        3: 1,
        4: 2,
        5: 2,
        6: 2,
        7: 1,
        8: 0,
        9: -1,
        10: -2,
        11: 0
    }
    hi_opt_1_card_values = {
        2: 0,
        3: 1,
        4: 1,
        5: 1,
        6: 1,
        7: 0,
        8: 0,
        9: 0,
        10: -1,
        11: 0
    }
    hi_opt_2_card_values = {
        2: 1,
        3: 1,
        4: 2,
        5: 2,
        6: 1,
        7: 1,
        8: 0,
        9: 0,
        10: -2,
        11: 0
    }
    # Advanced Card-Counting Algorithm card values
    wong_halves_card_values = {
        2: 0.5,
        3: 1,
        4: 1,
        5: 1.5,
        6: 1,
        7: 0.5,
        8: 0,
        9: -0.5,
        10: -1,
        11: -1
    }

    def check_bank(self):  # Ensures player bet does not exceed their bank balance
        if self.bank <= self.bet:
            self.bet = self.bank
        return self.bet

    def algorithm(self):  # Applies the algorithms based on specified card values
        self.running_count = dealt_cards.copy()
        for i in range(len(self.running_count)):
            self.running_count[i] = self.card_values[self.running_count[i]]
        self.running_count = sum(self.running_count)
        decks_played = len(dealt_cards) / len(std_deck)
        true_count = self.running_count / (num_decks - decks_played)
        if self.bank < 0.01:  # Stop player from betting if they have no money
            self.bet = 0
        elif self.bank > 0.01:
            if true_count >= 2:  # Alter the bet if the true count is 2 or exceeds 2
                self.change_bet(true_count)
            elif true_count < 2:
                self.bet = initial_bet  # Bet the minimum if true count less than 2
        self.bet = round(self.bet, 2)
        return self.check_bank()

    def change_bet(self, true_count):  # Changes the player bet using optimal betting formula
        if self.bank > 0.01:
            new_bet = (true_count - 1) * initial_bet
            self.bet = new_bet
        elif self.bank < 0.01:
            self.bet = 0
        return self.bet


class Player(Deal, Algorithms):
    def __init__(self, hand, score, new_card, running_count, card_values, bank, bet):
        super().__init__(hand, score, new_card, running_count, card_values)
        self.bank = bank
        self.bet = bet

    def blackjack(self):
        self.bank += 1.5 * self.bet
        high_low_player.bank += 1.5 * high_low_player.bet
        zen_count_player.bank += 1.5 * zen_count_player.bet
        omega_2_player.bank += 1.5 * omega_2_player.bet
        hi_opt_1_player.bank += 1.5 * hi_opt_1_player.bet
        hi_opt_2_player.bank += 1.5 * hi_opt_2_player.bet
        wong_halves_player.bank += 1.5 * wong_halves_player.bet
        return self.bank

    def win(self):
        self.bank += self.bet
        high_low_player.bank += high_low_player.bet
        zen_count_player.bank += zen_count_player.bet
        omega_2_player.bank += omega_2_player.bet
        hi_opt_1_player.bank += hi_opt_1_player.bet
        hi_opt_2_player.bank += hi_opt_2_player.bet
        wong_halves_player.bank += wong_halves_player.bet
        return self.bank

    def lose(self):
        self.bank -= self.bet
        high_low_player.bank -= high_low_player.bet
        zen_count_player.bank -= zen_count_player.bet
        omega_2_player.bank -= omega_2_player.bet
        hi_opt_1_player.bank -= hi_opt_1_player.bet
        hi_opt_2_player.bank -= hi_opt_2_player.bet
        wong_halves_player.bank -= wong_halves_player.bet
        return self.bank

    def push(self):
        self.bank = self.bank


class Dealer(Deal):
    pass


def need_reshuffle():  # Reshuffles shoe when shuffle percentage is reached
    global dealt_cards, shoe
    reshuffle_shoe_length = len(std_deck * num_decks) * shuffle_percentage
    if len(shoe) <= reshuffle_shoe_length:
        i = 0
        while i < len(dealt_cards):  # convert the value of all changed aces back to 11
            if dealt_cards[i] == 1:
                dealt_cards[i] = 11
            i += 1
        shoe += dealt_cards
        dealt_cards = []
        random.shuffle(shoe)
        return shoe


def blackjack_gameplay():
    global no_strategy_player, high_low_player, zen_count_player, \
           omega_2_player, hi_opt_1_player, hi_opt_2_player, wong_halves_player

    # Create the no strategy player and the dealer instances
    no_strategy_player = Player(hand, score, new_card, running_count, card_values, initial_bank, initial_bet)
    dealer = Dealer(hand, score, new_card, running_count, card_values)

    # Algorithmic players will have the exact same attributes as the no_strategy player
    high_low_player = deepcopy(no_strategy_player)
    zen_count_player = deepcopy(no_strategy_player)
    omega_2_player = deepcopy(no_strategy_player)
    hi_opt_1_player = deepcopy(no_strategy_player)
    hi_opt_2_player = deepcopy(no_strategy_player)
    wong_halves_player = deepcopy(no_strategy_player)

    # Algorithms take in different card values
    high_low_player.card_values = Algorithms.high_low_card_values
    zen_count_player.card_values = Algorithms.zen_count_card_values
    omega_2_player.card_values = Algorithms.omega_2_card_values
    hi_opt_1_player.card_values = Algorithms.hi_opt_1_card_values
    hi_opt_2_player.card_values = Algorithms.hi_opt_2_card_values
    wong_halves_player.card_values = Algorithms.wong_halves_card_values

    game_plays = 0
    while game_plays < 1000 and no_strategy_player.bank > 0:
        if no_strategy_player.bet >= no_strategy_player.bank:
            no_strategy_player.bet = no_strategy_player.bank  # Bet cannot exceed bank balance
        else:
            no_strategy_player.bet = initial_bet
        no_strategy_player.deal_initial_hand()
        dealer.deal_initial_hand()
        while no_strategy_player.score < 17:  # Player hits if their score is less than 17
            no_strategy_player.hit()
        while dealer.score <= 16:  # Dealer hits if their score is 16 or less
            dealer.hit()
        if no_strategy_player.score > 21:
            no_strategy_player.lose()
        elif no_strategy_player.score == dealer.score:
            no_strategy_player.push()
        elif no_strategy_player.score == 21:
            no_strategy_player.blackjack()
        elif no_strategy_player.score < dealer.score:
            if dealer.score > 21:
                no_strategy_player.win()
            elif dealer.score <= 21:
                no_strategy_player.lose()
        elif no_strategy_player.score > dealer.score:
            no_strategy_player.win()

        high_low_player.algorithm()
        zen_count_player.algorithm()
        omega_2_player.algorithm()
        hi_opt_1_player.algorithm()
        hi_opt_2_player.algorithm()
        wong_halves_player.algorithm()

        game_plays += 1


# ----- Run Monte Carlo Simulations -----
no_strategy_data = []
high_low_data = []
zen_count_data = []
omega_2_data = []
hi_opt_1_data = []
hi_opt_2_data = []
wong_halves_data = []

x = 0
while x < simulations:
    global no_strategy_player, high_low_player, zen_count_player, \
        omega_2_player, hi_opt_1_player, hi_opt_2_player, wong_halves_player

    blackjack_gameplay()

    # Store data of each player's profit/loss using different algorithms
    no_strategy_data.append(no_strategy_player.bank - initial_bank)
    high_low_data.append(high_low_player.bank - initial_bank)
    zen_count_data.append(zen_count_player.bank - initial_bank)
    omega_2_data.append(omega_2_player.bank - initial_bank)
    hi_opt_1_data.append(hi_opt_1_player.bank - initial_bank)
    hi_opt_2_data.append(hi_opt_2_player.bank - initial_bank)
    wong_halves_data.append(wong_halves_player.bank - initial_bank)

    x += 1

# ----- Crate a DataFrame to store Player Profit/Loss with different algorithms -----
df = pd.DataFrame(list(zip(no_strategy_data, high_low_data, zen_count_data,
                           omega_2_data, hi_opt_1_data, hi_opt_2_data, wong_halves_data)),
                  columns=['No Strategy P/L', 'High/Low P/L', 'Zen count P/L',
                           'Omega 2 P/L', 'Hi Opt 1 P/L', 'Hi Opt 2 P/L', 'Wong Halves P/L'])


# Compute the average Profit/Loss of each algorithm
no_strategy_average = round(df['No Strategy P/L'].mean(), 2)
high_low_average = round(df['High/Low P/L'].mean(), 2)
zen_count_average = round(df['Zen count P/L'].mean(), 2)
omega_2_average = round(df['Omega 2 P/L'].mean(), 2)
hi_opt_1_average = round(df['Hi Opt 1 P/L'].mean(), 2)
hi_opt_2_average = round(df['Hi Opt 2 P/L'].mean(), 2)
wong_halves_average = round(df['Wong Halves P/L'].mean(), 2)


# Calculate relative performance of an algorithm
def compute_rp(algo_avg):
    rp = round(((algo_avg/initial_bank) -
               (no_strategy_average/initial_bank)) * 100, 2)
    return rp


# ----- Plotting the results -----
x_axis = ['High/Low', 'Zen Count', 'Omega 2', 'Hi Opt 1', 'Hi Opt 2', 'Wong Halves']
y_axis = [
        compute_rp(high_low_average),
        compute_rp(zen_count_average),
        compute_rp(omega_2_average),
        compute_rp(hi_opt_1_average),
        compute_rp(hi_opt_2_average),
        compute_rp(wong_halves_average)]

plt.bar(x_axis, y_axis)
plt.title('Blackjack Card Counting Algorithm Comparison')
plt.xlabel('Algorithm')
plt.ylabel('Relative Performance (%)')

# Display the value of each bar
for index, data in enumerate(y_axis):
    plt.text(x=index-.1, y=data+.1, s=f"{data}%", fontdict=dict(fontsize=10))


# Create an average profits/losses dataframe
rp_data = {'Algorithm': [
    'No Strategy',
    'High/Low',
    'Zen Count',
    'Omega 2',
    'Hi Opt 1',
    'Hi Opt 2',
    'Wong Halves'],
    'Average Profit/Loss ($)': [
        no_strategy_average,
        high_low_average,
        zen_count_average,
        omega_2_average,
        hi_opt_1_average,
        hi_opt_2_average,
        wong_halves_average]
}

rp_df = pd.DataFrame(rp_data)

# Sort columns by relative performance
rp_df = rp_df.sort_values('Average Profit/Loss ($)', ascending=False)

# Change index to Ranking
rp_df = rp_df.reset_index(drop=True)
rp_df.index.name = 'Ranking'
rp_df.index += 1

print(tabulate(rp_df, headers='keys', tablefmt='psql'))

plt.show()
