# trie_standard.py

import sys

class StandardTrieNode:
    def __init__(self):
        self.children = {}
        self.index = None  # Index of the sequence if it's the end of a sequence

class StandardTrie:
    def __init__(self):
        self.root = StandardTrieNode()
        self.memory_usage = sys.getsizeof(self.root)
        self.dictionary_size = 0

    def insert(self, sequence, index):
        current_node = self.root
        new_entry = False  # Track if we are adding a new entry

        for byte in sequence:
            if byte not in current_node.children:
                current_node.children[byte] = StandardTrieNode()
                self.memory_usage += sys.getsizeof(current_node.children[byte])
                new_entry = True  # A new node indicates we are adding a new substring

            current_node = current_node.children[byte]

        if current_node.index is None:
            # Only increase dictionary size if this is a new entry
            self.dictionary_size += 1
            current_node.index = index

    def search(self, sequence):
        current_node = self.root
        for byte in sequence:
            if byte not in current_node.children:
                return None
            current_node = current_node.children[byte]
        return current_node.index

    def remove(self, sequence):
        # Helper function to recursively remove nodes
        def _remove(node, sequence, depth):
            if depth == len(sequence):
                # Reached the end of the sequence
                if node.index is not None:
                    node.index = None  # Remove the index
                    return len(node.children) == 0  # If no children, indicate this node can be deleted
                return False

            # Get the current character in the sequence
            byte = sequence[depth]
            if byte not in node.children:
                return False  # Sequence does not exist in the trie

            # Recursively call _remove on the child node
            child_node = node.children[byte]
            should_delete_child = _remove(child_node, sequence, depth + 1)

            # If the child node should be deleted, remove it from the children dictionary
            if should_delete_child:
                del node.children[byte]
                self.memory_usage -= sys.getsizeof(child_node)

                # Return true if this node also has no index and no other children
                return len(node.children) == 0 and node.index is None

            return False

        # Start removal from the root node
        _remove(self.root, sequence, 0)

    def get_dictionary_size(self):
        return self.dictionary_size

    def get_memory_usage(self):
        return self.memory_usage

    def visualize_trie(self):
        # Helper function to visualize the trie structure recursively, showing full strings
        def _visualize(node, current_string, level):
            if node.index is not None:
                # If this node has an index, it's a complete sequence
                print("  " * level + f"'{current_string}' (Index: {node.index})")

            # Traverse all children nodes
            for byte, child in node.children.items():
                _visualize(child, current_string + chr(byte), level + 1)

        print("Standard Trie Structure:")
        _visualize(self.root, "", 0)
