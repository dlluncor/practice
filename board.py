import sys

class Node(object):

  def __init__(self, letter, boost, x_pos, y_pos):
    self._letter = letter
    self._boost = boost
    self._x = x_pos
    self._y = y_pos

  def __str__(self):
    return '{0} - {1}. X:{2} Y: {3}'.format(
        self._letter, self._boost, self._x, self._y)

class Path(object):

  def __init__(self, start_node):
    self._path = [start_node]


class BoggleBoard(object):

  def __init__(self, nodes_2d):
    self.nodes_2d = nodes_2d

  def _add_to_paths(self, paths):

    for nodes in self.nodes_2d:
      for node in nodes:
        path = Path(node)

  def solve(self):
    paths = []
    self._add_to_paths(paths)

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