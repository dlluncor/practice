import sys

class Node(object):

  def __init__(self, letter, boost):
    self._letter = letter
    self._boost = boost

  def __repr__(self):
    return '{0} - {1}'.format(self._letter, self._boost)

  def __str__(self):
    return '{0} - {1}'.format(self._letter, self._boost)

class BoggleBoard(object):

  def __init__(self, nodes_2d):
    self.nodes_2d = nodes_2d

  @staticmethod
  def fromfile(txt):
    lines = txt.split('\n')
    nodes_2d = []

    for line in lines:
      nodes = []
      text_parts = line.split(' ')
      for text_part in text_parts:
        letter = text_part[0]
        boost = text_part[2:-1]
        node = Node(letter, boost)
        nodes.append(node)

      nodes_2d.append(nodes)

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

if __name__ == '__main__':
  main()