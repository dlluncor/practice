import sys
import enchant
import trie
import time
from boggle_constants import *

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

class Node(object):

  def __init__(self, letter, boost, x_pos, y_pos):
    if letter == 'q':
      letter = 'qu'

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

  def get_value(self, debug=False):
    word = ''
    total = 0
    total_mult = 1

    for node in self._nodes:
      word += node.get_letter()
      letter_val, word_mult = node.get_value()
      total += letter_val
      total_mult *= word_mult
      if debug:
        print('{0} {1}'.format(node.get_letter(), letter_val))

    len_val = len_add[len(word)]

    if debug:
      print('{0}, {1}, {2}, {3}'.format(word, total, len_val, total_mult))

    total = (total * total_mult) + len_val

    return (total, word)

# x, y
"""

0,0 1,0 2,0 3,0
0,1 1,1 2,1 3,1
0,2 1,2 2,2 3,2
0,3 1,3 2,3 3,3

"""

class Searcher(object):

  def __init__(self, nodes_2d, checker):
    self._nodes_2d = nodes_2d
    self._paths = []
    self._checker = checker
    #self._paths_considered = 0

  def add_a_neighbor(self, path, unused):
    #self._paths_considered += 1
    #if self._paths_considered % 1000:
    #  print('Starting at {0}, considered {1}'.format(
    #      path.first(), self._paths_considered))

    cur_node = path.last_node()

    neighs = neighbors[(cur_node.x, cur_node.y)]
    for neighbor in neighs:
      if neighbor not in unused:
        # its already used cant use it again
        continue

      new_path = path.copy()
      new_node = self._nodes_2d[neighbor[1]][neighbor[0]]
      new_path.add_node(new_node)
      word = new_path.as_word()

      is_prefix = self._checker.is_prefix(word)
      if not is_prefix:
        continue

      new_unused = dict(unused)
      del new_unused[neighbor]

      # Check if its a valid word (eventually prefix as well)

      if self._checker.is_word(word) and len(word) > 1:
        #print(word)
        self._paths.append(new_path)

      if is_prefix:
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
    write = self._p.write

    seen = {}
    for path in paths:

      val, word = path.get_value()
      if word in seen and val > seen[word]:
        seen[word] = val
      else:
        seen[word] = val

    word_vals = [(word, val) for word, val in seen.iteritems()]
    word_vals = sorted(word_vals, key=lambda x: x[1], reverse=True)

    write('Found {0} words'.format(len(word_vals)))

    words_list = []
    total = 0
    i = 0
    top_100 = 0

    for word, val in word_vals:
      total += val
      words_list.append('{0} {1}'.format(word, val))
      
      if i > 100:
        continue
      
      top_100 = total
      i += 1

    write('Top 100 words: {0} points'.format(top_100))
    write('Total possible: {0} points'.format(total))
    write('')
    write('\n'.join(words_list))


  def set_checker(self, checker):
    self._checker = checker

  def set_printer(self, printer):
    self._p = printer

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
      if not line:
        continue
      x = 0
      nodes = []
      text_parts = line.split(' ')

      for text_part in text_parts:
        letter = text_part[0]
        boost = text_part[1:]
        node = Node(letter, boost, x, y)
        nodes.append(node)
        x += 1

      nodes_2d.append(nodes)
      y += 1

    if y != 4:
      print('Incorrect number of lines {0}. Need 4'.format(y))
      sys.exit(1)

    return BoggleBoard(nodes_2d)

def load_wordlist():
  with open('dictionary.csv') as f:
    data = f.read()
  return data.split('\r\n')

class Printer(object):

  def __init__(self):
    self.f = open('out.txt', 'w')

  def write(self, w):
    if not isinstance(w, basestring):
      w = u'{0}'.format(w)

    print(w)
    self.f.write(w + '\n')

  def flush(self):
    self.f.close()

def main():
  
  board_txt = ''
  if len(sys.argv) == 1:
    print('Write the board:')
    board_txt = ''
    for i in xrange(4):
      board_txt += raw_input()
      board_txt += '\n' 
  elif len(sys.argv) == 2:
    with open(sys.argv[1]) as f:
      board_txt = f.read()
  else:
    print('Need to specify a filename or nothing')
    return

  p = Printer()

  one = time.time()

  checker = Checker()
  checker.load_from_words(load_wordlist())

  two = time.time()
  #print('Loading trie took {0} s'.format(two - one))

  board = BoggleBoard.fromfile(board_txt)
  board.set_checker(checker)
  board.set_printer(p)
  p.write(board)

  one = time.time()

  board.solve()

  two = time.time()

  p.write('Solving the puzzle took {0} s'.format(two - one))
  p.flush()

if __name__ == '__main__':
  main()
