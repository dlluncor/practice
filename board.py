import sys
import enchant
import trie
import time
from nltk.corpus import words

letter_val_d = dict(
  a=1, #
  b=4, #
  c=4, #
  d=2, #
  e=1, #
  f=4, #
  g=3, #
  h=3, #
  i=1, #
  j=10, #
  k=5, #
  l=2, #
  m=4, #
  n=2, #
  o=1, #
  p=4, #
qu=10, #
  r=1, #
  s=1, #
  t=1, #
  u=2, #
  v=5, #
  w=4, #
  x=8, #
  y=3, #
  z=10 #
)

class Checker(object):

  def __init__(self):
    self._trie = trie.Trie()

  def load_from_words(self, words_list):
    for word in words_list:
      self._trie.insert(word.lower())

  def is_prefix(self, word):
    return self._trie.startsWith(word.lower())

  def is_word(self, word):
    return self._trie.search(word.lower())

color_to_boost = {
  '': '',
  'b': '2l',
  'r': '2w',
  'g': '3l',
  'y': '3w'
}

class Node(object):

  def __init__(self, letter, boost, x_pos, y_pos):
    self._letter = letter
    self._boost = color_to_boost[boost]
    self.x = x_pos
    self.y = y_pos
    self._letter_val = letter_val_d[letter]

  def get_letter(self):
    return self._letter

  def get_value(self):
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

    return self._letter_val * letter_mult, word_mult

  def __str__(self):
    return '{0} - {1}. ({2}, {3})'.format(
        self._letter, self._boost, self.x, self.y)

len_add = {
    2: 0,
    3: 0,
    4: 0,
    5: 3,
    6: 6,
    7: 10,
    8: 15,
    9: 20,
    10: 25
}

class Path(object):

  def __init__(self, nodes):
    self._nodes = nodes

  def add_node(self, node):
    self._nodes.append(node)

  def first(self):
    return self._nodes[0]

  def last_node(self):
    return self._nodes[-1]

  def copy(self):
    return Path(list(self._nodes))

  def as_word(self):
    s = ''
    for node in self._nodes:
      s += node.get_letter()
    return s

  def get_value(self):
    word = ''
    total = 0
    total_mult = 1

    for node in self._nodes:
      word += node.get_letter()
      letter_val, word_mult = node.get_value()
      total += letter_val
      total_mult *= word_mult

    total += len_add[len(word)]

    return (total * total_mult, word)

default_unused = {
  (0, 0): False,
  (0, 1): False,
  (0, 2): False,
  (0, 3): False,
  (1, 0): False,
  (1, 1): False,
  (1, 2): False,
  (1, 3): False,
  (2, 0): False,
  (2, 1): False,
  (2, 2): False,
  (2, 3): False,
  (3, 0): False,
  (3, 1): False,
  (3, 2): False,
  (3, 3): False,
}

# x, y
"""

0,0 1,0 2,0 3,0
0,1 1,1 2,1 3,1
0,2 1,2 2,2 3,2
0,3 1,3 2,3 3,3

"""

neighbors = {
  (0, 0): [(1, 0), (0, 1), (1, 1)],
  (0, 1): [(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)],
  (0, 2): [(0, 1), (1, 1), (1, 2), (1, 3), (0, 3)],
  (0, 3): [(0, 2), (1, 2), (1, 3)],
  (1, 0): [(0, 0), (0, 1), (1, 1), (2, 1), (2, 0)],
  (1, 1): [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)],
  (1, 2): [(0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (2, 2), (2, 1), (1, 1)],
  (1, 3): [(0, 3), (0, 2), (1, 2), (2, 2), (2, 3)],
  (2, 0): [(1, 0), (1, 1), (2, 1), (3, 1), (3, 0)],
  (2, 1): [(1, 0), (1, 1), (1, 2), (2, 2), (3, 2), (3, 1), (3, 0), (2, 0)],
  (2, 2): [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (2, 1)],
  (2, 3): [(1, 3), (1, 2), (2, 2), (3, 2), (3, 3)],
  (3, 0): [(2, 0), (2, 1), (3, 1)],
  (3, 1): [(3, 0), (2, 0), (2, 1), (2, 2), (3, 2)],
  (3, 2): [(3, 3), (2, 3), (2, 2), (2, 1), (3, 1)],
  (3, 3): [(2, 3), (2, 2), (3, 2)], 
}

class Searcher(object):

  def __init__(self, nodes_2d, checker):
    self._nodes_2d = nodes_2d
    self._paths = []
    self._checker = checker
    self._paths_considered = 0

  def add_a_neighbor(self, path, unused):
    self._paths_considered += 1
    #if self._paths_considered % 1000:
    #  print('Starting at {0}, considered {1}'.format(
    #      path.first(), self._paths_considered))

    cur_node = path.last_node()

    neighs = neighbors[(cur_node.x, cur_node.y)]
    for neighbor in neighs:
      if neighbor not in unused:
        # its already used cant use it again
        continue

      # We can add this neighbor
      new_path = path.copy()
      new_unused = dict(unused)
      del new_unused[neighbor]
      new_node = self._nodes_2d[neighbor[1]][neighbor[0]]
      new_path.add_node(new_node)

      # Check if its a valid word (eventually prefix as well)
      word = new_path.as_word()
      if self._checker.is_word(word) and len(word) > 1:
        #print(word)
        self._paths.append(new_path)

      if self._checker.is_prefix(word):
        # Continue on search if its indeed a prefix.
        self.add_a_neighbor(new_path, new_unused)

  def get_all_paths(self, start_node):
    node = start_node
    unused = dict(default_unused)
    del unused[(node.x, node.y)]
    path = Path([node])
    self.add_a_neighbor(path, unused)

    #print('Considered {0} total'.format(self._paths_considered))
    return self._paths

class BoggleBoard(object):

  def __init__(self, nodes_2d):
    self.nodes_2d = nodes_2d

  def _find_paths(self):
    if not self._checker:
      return

    all_paths = []

    for nodes in self.nodes_2d:
      for node in nodes:
        searcher = Searcher(self.nodes_2d, self._checker)
        paths = searcher.get_all_paths(node)
        all_paths.extend(paths)

    return all_paths

  def solve(self):
    paths = self._find_paths()

    #paths = [Path([(1, 1), (0, 0), (1, 0), (0, 1)])] # fade

    seen = {}
    for path in paths:
      val, word = path.get_value()
      if word in seen and val > seen[word]:
        seen[word] = val
      else:
        seen[word] = val

    word_vals = [(word, val) for word, val in seen.iteritems()]

    word_vals = sorted(word_vals, key=lambda x: x[1], reverse=True)

    print('Found {0} words'.format(len(word_vals)))

    for word, val in word_vals:
      print('{0} {1}'.format(word, val))

    #self._add_to_paths(paths)

  def set_checker(self, checker):
    self._checker = checker

  def __str__(self):
    lines = []
    for nodes in self.nodes_2d:
      s = ''
      for node in nodes:
        s += ' ' + str(node)
      lines.append(s)
    return '\n'.join(lines)

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

  one = time.time()

  checker = Checker()
  checker.load_from_words(words.words())

  two = time.time()
  #print('Loading trie took {0} s'.format(two - one))

  with open(sys.argv[1]) as f:
    board_txt = f.read()

  board = BoggleBoard.fromfile(board_txt)
  board.set_checker(checker)
  print(board)

  one = time.time()

  board.solve()

  two = time.time()

  print('Solving the puzzle took {0} s'.format(two - one))

if __name__ == '__main__':
  main()