import random


class Game:
    barrel_value_min = 1
    barrel_value_max = 90

    def __init__(self, players):
        self.bag = Bag(self.barrel_value_min, self.barrel_value_max)
        self.players = players
        for player in self.players:
            player.card = Card(self.barrel_value_min, self.barrel_value_max)
        self.player_n = len(self.players)

    def step(self):
        barrel = self.bag.get_barrel()
        print(f'New barrel is {barrel}. There are {len(self.bag)} barrels in the bag')
        for i, player in enumerate(self.players):
            if not player.is_out_of_game:
                print(f'Player #{i + 1} card')
                print(player.card)
                player_can_continue = player.check(barrel)
                if player_can_continue:
                    if player.is_winner:
                        print(f'Player #{i + 1} win')
                        return False
                else:
                    print(f'Player #{i + 1} is out of the game')
                    self.player_n -= 1

        return self.player_n > 0


class Bag:
    def __init__(self, barrel_value_min, barrel_value_max):
        self.barrels = list(range(barrel_value_min, barrel_value_max + 1))
        random.shuffle(self.barrels)

    def get_barrel(self):
        return self.barrels.pop()

    def __len__(self):
        return len(self.barrels)


class Player:
    def __init__(self):
        self.card = None
        self.is_out_of_game = False

    @property
    def is_winner(self):
        return self.card.all_numbers_crossed_out


class HumanPlayer(Player):
    def check(self, barrel):
        if self.select_cross_out():
            print('Player crossed out the barrel')
            if barrel in self.card:
                self.card.cross_out(barrel)
                return True
            else:
                self.is_out_of_game = True
                return False
        else:
            print('Player skipped the barrel')
            if barrel in self.card:
                self.is_out_of_game = True
                return False
            else:
                return True

    @staticmethod
    def select_cross_out():
        return input('Would you like to cross the barrel out (no means skip)? (y/n): ').lower() == 'y'


class ComputerPlayer(Player):
    def check(self, barrel):
        if barrel in self.card:
            print('Player crossed out the barrel')
            self.card.cross_out(barrel)
        else:
            print('Player skipped the barrel')
        return True


class Card:
    card_col_n = 9
    card_row_n = 3
    card_value_n = 5

    def __init__(self, card_value_min, card_value_max):
        row_values = list(range(card_value_min, card_value_max + 1))
        random.shuffle(row_values)
        self.numbers_array = list()
        for row_i in range(self.card_row_n):
            col_indexes = list()
            col_n = 0
            while col_n < self.card_value_n:
                col_i = random.randint(0, self.card_col_n - 1)
                if col_i not in col_indexes:
                    col_indexes.append(col_i)
                    col_n += 1

            row = [None] * self.card_col_n
            for i, col_i in enumerate(col_indexes):
                row[col_i] = row_values.pop()
            self.numbers_array.append(row)
        self.crossed_n = 0

    def __str__(self):
        return '\n'.join(
            [' '.join([str(v).rjust(2, ' ') if v is not None else '  ' for v in row]) for row in self.numbers_array])

    @property
    def all_numbers_crossed_out(self):
        return self.crossed_n == self.card_row_n * self.card_value_n

    def cross_out(self, barrel):
        for row_i, row in enumerate(self.numbers_array):
            try:
                col_i = row.index(barrel)
                self.numbers_array[row_i][col_i] = '--'
                self.crossed_n += 1
            except ValueError:
                pass

    def __contains__(self, barrel):
        for row in self.numbers_array:
            if barrel in row:
                return True
        return False


def run_game():
    print('Lotto game')
    print('1 - Human vs Human')
    print('2 - Human vs Computer')
    print('3 - Computer vs Computer')
    print('4 - Company of friends')
    game_type_id = int(input('Select type of game please (1-4): '))

    players = list()
    if game_type_id == 1:
        players.append(HumanPlayer())
        players.append(HumanPlayer())
    elif game_type_id == 2:
        players.append(HumanPlayer())
        players.append(ComputerPlayer())
    elif game_type_id == 3:
        players.append(ComputerPlayer())
        players.append(ComputerPlayer())
    elif game_type_id == 4:
        players_n = int(input('How many friends are going to join the game: '))
        for i in range(players_n):
            players.append(HumanPlayer())
    game = Game(players)
    while game.step():
        input('Press any key to continue')


if __name__ == '__main__':
    run_game()
