import random
import csv
import datetime

class Board:
  def __init__(self):
    self._rows = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

  def __str__(self):
    s = '-------\n'
    for row in self._rows:
      for cell in row:
        s = s + '|'
        if cell == None:
          s=s+' '
        else:
          s=s+cell
      s = s + '|\n-------\n'
    return s

  def get(self, x, y):
    return self._rows[y][x]

  def set(self, x, y, value):
    self._rows[y][x] = value

  def is_full(self):
        return all(cell is not None for row in self._rows for cell in row)


  def get_winner(self):
        for i in range(3):
            if self._rows[i][0] == self._rows[i][1] == self._rows[i][2] is not None or \
               self._rows[0][i] == self._rows[1][i] == self._rows[2][i] is not None:
                return True
        if self._rows[0][0] == self._rows[1][1] == self._rows[2][2] is not None or \
           self._rows[0][2] == self._rows[1][1] == self._rows[2][0] is not None:
            return True
        return False

class Game:
    def __init__(self, playerX, playerO):     
        self._board = Board()
        self._playerX = playerX
        self._playerO = playerO
        self._current_player = self._playerX
        self.moves_count = 0

    def log_game_result(self, winner):
        with open('game_logs.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([date_time, self._playerX.__class__.__name__, self._playerO.__class__.__name__, winner, self.moves_count])

    def run(self):
        while not self._board.is_full() and not self._board.get_winner():
            print(self._board)
            move = self._current_player.get_move(self._board)
            x, y = move
            if self._board.get(x, y) is None:
                self._board.set(x, y, 'X' if self._current_player == self._playerX else 'O')
                self._current_player = self._playerO if self._current_player == self._playerX else self._playerX
                self.moves_count += 1
            else:
                print("Invalid move. Try again.")

        print(self._board)
        if self._board.get_winner():
            print("We have a winner!")
            winner = 'O' if self._current_player == self._playerX else 'X'  # Corrected winner determination
        else:
            print("It's a draw!")
            winner = 'Draw'
        self.log_game_result(winner)


class Human:
    def get_move(self, board):
        move = input("Enter your move (x y): ").split()
        return int(move[0]), int(move[1])

class Bot:
    def get_move(self, board):
        available_moves = [(x, y) for x in range(3) for y in range(3) if board.get(x, y) is None]
        return random.choice(available_moves) if available_moves else (None, None)

# Main game execution
player_choice = input("Choose 1 for single player or 2 for two players: ")
if player_choice == "1":
    game = Game(Human(), Bot())
else:
    game = Game(Human(), Human())
game.run()
