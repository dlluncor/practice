import sys

letter_val_d = dict(
  a=1,
  b=2,
  c=3,
  d=2,
  e=1,
  f=4,
  g=3,
  h=4,
  i=1,
  j=5,
  k=5,
  l=2,
  m=3,
  n=2,
  o=2,
  p=3,
  q=10,
  r=1,
  s=1,
  t=2,
  u=2,
  v=5,
  w=5,
  x=8,
  y=5,
  z=10
)

valid_words = set(['fade', 'ade'])

def is_word(word):
  return word in valid_words

class Node(object):

  def __init__(self, letter, boost, x_pos, y_pos):
    self._letter = letter
    self._boost = boost
    self._x = x_pos
    self._y = y_pos
    self._letter_val = letter_val_d[letter]

  def get_letter(self):
    return self._letter

  def add_value(self, cur_val):
    b = self._boost
    word_mult = 1
    letter_mult = 1

    if b == '2w':
      word_mult = 2
    elif b == '3w':
      word_mult = 3
    elif b == '2l':
      letter_mult = 2
    elif b == '3l':
      letter_mult = 3

    return (cur_val + (self._letter_val * letter_mult)) * word_mult

  def __str__(self):
    return '{0} - {1}. ({2}, {3})'.format(
        self._letter, self._boost, self._x, self._y)

class Path(object):

  def __init__(self, indices):
    self._indices = indices

  def get_value(self, nodes_2d):
    word = ''
    val = 0
    for (x, y) in self._indices:
      node = nodes_2d[y][x]
      word += node.get_letter()
      val = node.add_value(val)

    if is_word(word):
      return (val, word) 

    return (0, word)

class BoggleBoard(object):

  def __init__(self, nodes_2d):
    self.nodes_2d = nodes_2d

  def _add_to_paths(self, paths):

    for nodes in self.nodes_2d:
      for node in nodes:
        path = Path(node, self.nodes_2d, dict())
        found_paths = path.search()
        print(found_paths)

  def solve(self):
    paths = [
      Path([(1, 1), (0, 0), (1, 0), (0, 1)]), # fade
    ]
    for path in paths:
      val, word = path.get_value(self.nodes_2d)
      print('{0} - {1}'.format(word, val))

    #self._add_to_paths(paths)

  @staticmethod
  def fromfile(txt):
    lines = txt.split('\n')
    nodes_2d = []

    y = 0
    for line in lines:

      x = 0
      nodes = []
      text_parts = line.split(' ')

      for text_part in text_parts:
        letter = text_part[0]
        boost = text_part[2:-1]
        node = Node(letter, boost, x, y)
        nodes.append(node)
        x += 1

      nodes_2d.append(nodes)
      y += 1

    return BoggleBoard(nodes_2d)

def main():
  if len(sys.argv) != 2:
    print('Need to have at least two arguments')
    return

  with open(sys.argv[1]) as f:
    board_txt = f.read()

  print(board_txt)
  board = BoggleBoard.fromfile(board_txt)
  for nodes in board.nodes_2d:
    s = ''
    for node in nodes:
      s += ' ' + str(node)
    print(s)

  board.solve()

if __name__ == '__main__':
  main()