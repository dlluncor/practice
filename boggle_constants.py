import sys

from typing import Text

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

def value_of(word):
  # type: (Text) -> Text
  w = ''
  for letter in word:
    w += ' {0}'.format(letter_val_d[letter])

  return w

color_to_boost = {
  '': '',
  'b': '2l',
  'r': '2w',
  'g': '3l',
  'G': '3w'
}

len_add = {
    2: 0,
    3: 0,
    4: 0,
    5: 3,
    6: 6,
    7: 10,
    8: 15,
    9: 20,
    10: 25,
    11: 30,
    12: 35,
    13: 40,
    14: 45,
    15: 50,
    16: 55
}


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

for k, neighs in neighbors.items():
  for neigh in neighs:
    if k == neigh:
      print('Repeat. Invalid neighbor for key {0}'.format(k))
      sys.exit(1)
    if abs(k[0] - neigh[0]) > 1:
      print('x wrong. Invalid neighbor for key {0}'.format(k))
      sys.exit(1)
    if abs(k[1] - neigh[1]) > 1:
      print('y wrong. Invalid neighbor for key {0}'.format(k))
      sys.exit(1)
