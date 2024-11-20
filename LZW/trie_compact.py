# trie_compact.py

import sys

class CompactTrieNode:
    def __init__(self):
        self.children = {}
        self.index = None

class CompactTrie:
    def __init__(self):
        self.root = CompactTrieNode()
        self.memory_usage = sys.getsizeof(self.root)
        self.dictionary_size = 0  # Track the number of unique substrings added

    def insert(self, sequence, index):
        current_node = self.root
        while sequence:
            found_prefix = False
            for child_key in list(current_node.children.keys()):
                prefix_length = self._common_prefix_length(sequence, child_key)

                if prefix_length > 0:
                    found_prefix = True

                    # Full match of the current prefix with the child key
                    if prefix_length == len(child_key):
                        current_node = current_node.children[child_key]
                        sequence = sequence[prefix_length:]
                    else:
                        # Partial match, splitting the node
                        existing_child = current_node.children.pop(child_key)

                        # Create a new split node for the common prefix
                        split_node = CompactTrieNode()
                        self.memory_usage += sys.getsizeof(split_node)

                        split_node.children[child_key[prefix_length:]] = existing_child
                        self.memory_usage += sys.getsizeof(existing_child)

                        # Add the split node under the common prefix
                        current_node.children[child_key[:prefix_length]] = split_node
                        self.memory_usage += sys.getsizeof(child_key[:prefix_length])

                        # Add the remaining part of the new sequence as a new node
                        if len(sequence) > prefix_length:
                            new_node = CompactTrieNode()
                            self.memory_usage += sys.getsizeof(new_node)
                            split_node.children[sequence[prefix_length:]] = new_node
                            new_node.index = index
                            self.dictionary_size += 1  # Count this as a new dictionary entry
                        else:
                            split_node.index = index

                        # Count the split node as a new entry only if it was newly added
                        self.dictionary_size += 1
                        return
                    break

            # If no common prefix is found, add the sequence as a new branch
            if not found_prefix:
                new_node = CompactTrieNode()
                self.memory_usage += sys.getsizeof(new_node)
                current_node.children[sequence] = new_node
                new_node.index = index
                self.dictionary_size += 1  # Count this as a new dictionary entry
                return

    def search(self, sequence):
        current_node = self.root
        while sequence:
            found_prefix = False
            for child_key in current_node.children.keys():
                prefix_length = self._common_prefix_length(sequence, child_key)

                # Check if we have a full match with the child key
                if prefix_length == len(child_key):
                    # Move to the next level of the trie
                    current_node = current_node.children[child_key]
                    sequence = sequence[prefix_length:]
                    found_prefix = True
                    break

                # If we find an exact match of the sequence with the child_key
                elif prefix_length == len(sequence) and prefix_length == len(child_key):
                    return current_node.children[child_key].index

            if not found_prefix:
                return None

        return current_node.index

    def remove(self, sequence):
        # Helper function to recursively remove nodes and update the trie structure
        def _remove(node, sequence, depth):
            if depth == len(sequence):
                # Reached the end of the sequence
                if node.index is not None:
                    node.index = None  # Remove the index
                    # If this node has no children, indicate it can be deleted
                    return len(node.children) == 0
                return False

            # Get the current prefix length and child node
            for child_key in list(node.children.keys()):
                prefix_length = self._common_prefix_length(sequence[depth:], child_key)

                if prefix_length > 0:
                    # Traverse deeper if the current child_key matches the prefix
                    child_node = node.children[child_key]

                    # If the entire child_key matches the current part of the sequence
                    if prefix_length == len(child_key):
                        should_delete_child = _remove(child_node, sequence, depth + prefix_length)

                        # If the child node should be deleted, remove it from the children dictionary
                        if should_delete_child:
                            del node.children[child_key]
                            self.memory_usage -= sys.getsizeof(child_node)

                            # If the current node is now empty and does not have an index, delete it
                            return len(node.children) == 0 and node.index is None

                    # Handle cases where a partial prefix matches
                    elif prefix_length > 0 and prefix_length < len(child_key):
                        # The node is partially matched, which means removal ends here as the exact sequence isn't fully matched
                        return False

            return False

        # Start removal from the root node
        _remove(self.root, sequence, 0)

    def _common_prefix_length(self, word1, word2):
        # Helper method to calculate common prefix length
        min_length = min(len(word1), len(word2))
        for i in range(min_length):
            if word1[i] != word2[i]:
                return i
        return min_length

    def get_dictionary_size(self):
        return self.dictionary_size

    def get_memory_usage(self):
        return self.memory_usage

    def visualize_trie(self):
        # Helper function to visualize the trie structure recursively
        def _visualize(node, prefix, level):
            for child_key, child in node.children.items():
                child_prefix = prefix + child_key.decode()  # Convert bytes to a string for visualization
                if level > 0:
                    print("  " * (level - 1) + f"{child_key.decode()} (Index: {child.index})")
                _visualize(child, child_prefix, level + 1)

        print("Compact Trie Structure:")
        _visualize(self.root, "", 0)
