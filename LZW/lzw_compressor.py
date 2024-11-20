# lzw_compressor.py

import time
from trie_standard import StandardTrie
from trie_compact import CompactTrie

class LZWCompressor:
    def __init__(self, max_bits=12, use_compact_trie=False, fixedLZW=False):
        self.max_bits = max_bits
        self.max_table_size = 2 ** max_bits
        self.use_compact_trie = use_compact_trie
        self.trie = CompactTrie() if use_compact_trie else StandardTrie()
        self.fixedLZW = fixedLZW

    def compress(self, byte_sequence, generate_stats=False):
        start_time = time.time()

        # Initialize the dictionary with individual bytes (0-255)
        for i in range(256):
            self.trie.insert(bytes([i]), i)
        dict_size = 256

        current_sequence = bytes()
        compressed_data = []

        # Start with 9 bits
        current_bits = 9
        if self.fixedLZW:
            current_bits = self.max_bits
        max_dict_size = 2 ** current_bits

        for current_byte in byte_sequence:
            next_sequence = current_sequence + bytes([current_byte])
            if self.trie.search(next_sequence) is not None:
                current_sequence = next_sequence
            else:
                # Output the code for current_sequence
                compressed_data.append(self.trie.search(current_sequence))

                # Add next_sequence to the dictionary if size allows
                if dict_size < self.max_table_size:
                    if dict_size >= max_dict_size and current_bits < self.max_bits:
                        current_bits += 1
                        max_dict_size = 2 ** current_bits

                    self.trie.insert(next_sequence, dict_size)
                    dict_size += 1

                current_sequence = bytes([current_byte])

        # Output the code for the remaining sequence, if any
        if current_sequence:
            compressed_data.append(self.trie.search(current_sequence))

        end_time = time.time()
        compression_ratio = len(compressed_data) / len(byte_sequence)

        if generate_stats:
            stats = {
                'operation': 'compression',
                'ratio': compression_ratio,
                'dictionary_size': self.trie.get_dictionary_size(),  # Modified to use the trie method
                'memory_usage': self.trie.get_memory_usage(),
                'execution_time': end_time - start_time,
                'bits_used': current_bits
            }
            return compressed_data, stats

        return compressed_data
