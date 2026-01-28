
import json

with open("snippets.json", "r") as f:
    data = json.load(f)

keywords = data["keywords"]
snippets = data["snippets"]

import keyword

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def get_words_with_prefix(self, prefix):#DFS used
        def dfs(node, path, results):
            if node.is_end_of_word:
                results.append(path)
            for char, next_node in node.children.items():
                dfs(next_node, path + char, results)

        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        results = []
        dfs(node, prefix, results)
        return results

# Initialize the Trie and insert Python keywords
trie = Trie()
for word in keyword.kwlist:
    trie.insert(word)

def get_suggestions(prefix):
    return trie.get_words_with_prefix(prefix)

def expand_snippet(word):
    # Optional: you can add snippet expansions here
    snippets = {
        "fori": "for i in range():",
        "ifmain": "if __name__ == '__main__':",
    }
    return snippets.get(word, None)

