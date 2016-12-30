# Connect Four game

from itertools import groupby, cycle, dropwhile

class Cell:
  def __init__(self, c=None):
    self.c = c

Board = [[Cell() for _ in range(7)] for _ in range(6)]

Players = cycle(['X', 'O'])

def col(board, num):
  return [row[num] for row in board]
  
def diags(board, direction=1):
  "Return right diagonal; direction=-1 for left diagonal."
  l = len(board[0])
  return [[row[(n+i*direction)%l] for i, row in enumerate(board)] for n in range(l)]

def place(board, num, player):
  "Places peice on board. Returns -1 if column full."
  try:
    targ = next(c for c in reversed(col(board, num)) if not c.c)
  except StopIteration:
    return -1
  targ.c = player
  return
  
def display(board):
  print(' '.join(str(i) for i in range(len(board[0]))))
  for row in board:
    print(' '.join([c.c or '-' for c in row]))
  print()
  
def cols(board):
  return [col(board, num) for num in range(len(board[0]))]
  
def is_won(board, player, x=4):
  rows = board
  columns = cols(board)
  ldiags = diags(board)
  rdiags = diags(board, -1)
  return any(any(any(True for p, cs in groupby(line, lambda x: x.c) if p == player and len(list(cs)) >= x) 
  for line in lines) 
  for lines in [rows, columns, ldiags, rdiags])

# computer

from random import choice

def rand(board):
  "Random choice from free columns."
  spaces = [i for i, c in enumerate(cols(board)) if any(cell.c == None for cell in c)]
  return choice(spaces)
  
def copy_board(board):
  "Deep copies board (copies cells)."
  return [[Cell(cell.c) for cell in row] for row in board]
  
def x_in_row_move(board, targ, x):
  "Returns a move that give targ x in a row or None."
  boards = [copy_board(board) for _ in range(len(board[0]))]
  res = [column 
  for column, board in enumerate(boards) 
  if place(board, column, targ) != -1 and is_won(board, targ, x)]
  return choice(res or [None])
  
def dont_give_win(board, targ, own, x):
  "Returns a move that doesn't directly open a winning move for opponent."
  # todo
  boards = [copy_board(board) for _ in range(len(board[0]))]
  res = []
  for column, board in enumerate(boards):
    if place(board, column, own) != -1:
      place(board, column, targ)
      if not is_won(board, targ, x):
        res.append(column)
  return choice(res or [None])

def choose(board):
  col_num = (x_in_row_move(board, 'O', 4)
  or x_in_row_move(board, 'X', 4)
  or dont_give_win(board, 'X', 'O', 4)
  or rand(board)
  )
  return col_num

def validate_input(msg, fn, valids):
  while True:
    try:
      res = fn(input(msg))
    except ValueError:
      print('Invalid input - try again.')
      continue
    if res in valids:
      break
    else:
      print('Invalid input - try again.')
  return res

# main loop

print('\n\n== Connect Four ==\n')
while True:
  p = next(Players)
  display(Board)
  if p == 'X':
      move = validate_input('Move ('+p+'): ', int, list(range(len(Board[0]))))
  else:
    move = choose(Board)
  print()
  if place(Board, move, p) == -1:
    print('Column full - try again.')
    print()
    p = next(Players)
  if is_won(Board, p):
    display(Board)
    print()
    print(p + ' wins!')
    break
