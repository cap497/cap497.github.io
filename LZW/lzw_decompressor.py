# lzw_decompressor.py

import time
import sys
from trie_standard import StandardTrie
from trie_compact import CompactTrie

class LZWDecompressor:
    def __init__(self, max_bits=12, fixedLZW=False):
        self.max_bits = max_bits
        self.max_table_size = 2 ** max_bits
        self.fixedLZW = fixedLZW

    def decompress(self, compressed_data, generate_stats=False):
        start_time = time.time()

        # Initialize the dictionary with individual bytes (0-255)
        dictionary = {i: bytes([i]) for i in range(256)}
        dict_size = 256

        # Start with 9 bits
        current_bits = 9
        if self.fixedLZW:
            current_bits = self.max_bits
        max_dict_size = 2 ** current_bits

        if not compressed_data:
            raise ValueError("Compressed data is empty; nothing to decompress.")

        # Read the first code
        current_code = compressed_data.pop(0)
        if current_code >= dict_size:
            raise ValueError(f"Invalid code found during decompression: {current_code}")

        # Initialize the result with the first sequence
        current_sequence = dictionary[current_code]
        decompressed_data = bytearray(current_sequence)

        # Iterate through the remaining codes
        for code in compressed_data:
            # Check if the code is in the dictionary
            if code in dictionary:
                entry = dictionary[code]
            elif code == dict_size:
                # Handle the case where the code is not in the dictionary yet (LZW edge case)
                entry = current_sequence + current_sequence[0:1]
            else:
                raise ValueError(f"Invalid compressed code encountered: {code}")

            # Append the entry to the decompressed data
            decompressed_data.extend(entry)

            # Add new sequence to the dictionary
            if len(dictionary) < self.max_table_size:
                if dict_size >= max_dict_size and current_bits < self.max_bits:
                    current_bits += 1
                    max_dict_size = 2 ** current_bits

                dictionary[dict_size] = current_sequence + entry[0:1]
                dict_size += 1

            current_sequence = entry

        end_time = time.time()

        # Calculate decompression ratio
        decompressed_bits = len(decompressed_data) * 8
        compressed_bits = len(compressed_data) * current_bits + current_bits  # Include bits from the first code as well
        decompression_ratio = decompressed_bits / compressed_bits

        if generate_stats:
            stats = {
                'operation': 'decompression',
                'ratio': decompression_ratio,
                'dictionary_size': dict_size,
                'memory_usage': sys.getsizeof(dictionary) + sum(sys.getsizeof(v) for v in dictionary.values()),
                'execution_time': end_time - start_time,
                'bits_used': current_bits
            }
            return decompressed_data, stats

        return decompressed_data
