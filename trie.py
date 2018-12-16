from collections import defaultdict

from typing import Text, Dict

"""
  dawn: true
  david: true
  dawns

  d

  a

  v    w

  i    n
 
  d    s

  d -> ["a": {}]
  n -> {"_end": true, "s": true}
  s -> {"_end": true}

"""

class Trie(object):
    """
    Implement a trie with insert, search, and startsWith methods.
    """
    def __init__(self):
        # type: () -> None
        self.root = defaultdict() # type: Dict

    # @param {string} word
    # @return {void}
    # Inserts a word into the trie.
    def insert(self, word):
        # type: (Text) -> None
        current = self.root
        for letter in word:
            current = current.setdefault(letter, {})
        current.setdefault("_end")

    # @param {string} word
    # @return {boolean}
    # Returns if the word is in the trie.
    def search(self, word):
        # type: (Text) -> bool
        current = self.root
        for letter in word:
            if letter not in current:
                return False
            current = current[letter]
        if "_end" in current:
            return True
        return False

    # @param {string} prefix
    # @return {boolean}
    # Returns if there is any word in the trie
    # that starts with the given prefix.
    def startsWith(self, prefix):
        # type: (Text) -> bool
        current = self.root
        for letter in prefix:
            if letter not in current:
                return False
            current = current[letter]
        return True