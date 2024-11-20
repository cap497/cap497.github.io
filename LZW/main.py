import sys
import argparse
import nltk
from nltk.corpus import gutenberg
from lzw_compressor import LZWCompressor
from lzw_decompressor import LZWDecompressor
from plot import generate_graphs
import csv
import pandas as pd
import os

def text_to_bytes(text):
    """Convert text to bytes using UTF-8 encoding."""
    return text.encode('utf-8')

def bytes_to_text(byte_sequence):
    """Convert bytes to text using UTF-8 decoding."""
    return byte_sequence.decode('utf-8')

def main():
    # Download the Gutenberg corpus
    nltk.download('gutenberg')
    file_ids = gutenberg.fileids()

    # Set up command-line arguments
    parser = argparse.ArgumentParser(description="LZW Compression and Decompression with Compact and Standard Tries")
    parser.add_argument('--compact', action='store_true', help="Use Compact Trie for LZW")
    parser.add_argument('--fixed', action='store_true', help="Use fixed LZW bit length")
    parser.add_argument('--max-bits', type=int, help="Maximum number of bits", default=12)

    parser.add_argument('--test', nargs='?', const=len(file_ids), type=int, help="Run tests on the entire Gutenberg corpus or the first X number of files")
    parser.add_argument('--file', type=str, help="Path to a specific .txt file to use")
    parser.add_argument('--input', type=str, help="Input string to compress and decompress")

    parser.add_argument('--stats', action='store_true', help="Save statistics in stats.csv")
    parser.add_argument('--plot', action='store_true', help="Generate statistics graphs")

    args = parser.parse_args()

    use_compact = args.compact
    fixed_lzw = args.fixed
    max_bits = args.max_bits
    
    generate_stats = args.stats
    plot_graphs = args.plot

    # Determine the source of the input data
    if args.test is not None:
        # Run tests on the first X number of Gutenberg files or all files if no number is specified
        num_files = args.test
        test_files = file_ids[:num_files]
    elif args.file:
        # Read text from a provided .txt file
        try:
            with open(args.file, 'r', encoding='utf-8') as file:
                file_content = file.read()
            test_files = [(args.file, file_content)]
        except FileNotFoundError:
            print(f"Error: The file '{args.file}' was not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: An error occurred while reading the file: {e}")
            sys.exit(1)
    elif args.input:
        # Use the input text directly from the command line
        test_files = [("Input String", args.input)]
    else:
        print("Error: You must provide either an --input string, a --file, or use the --test option.")
        sys.exit(1)

    # Define different lengths for testing
    length_tests = {
        'Short (< 100 chars)': 100,
        'Medium (100 - 1000 chars)': 1000,
        'Long (1000 - 10000 chars)': 10000,
        'Huge (10000 - 100000 chars)': 100000
    }

    # Create a list to store all the statistics from each test
    all_stats = []

    # Process each file or input
    for input_info in test_files:
        file_id, raw_text = (input_info, gutenberg.raw(input_info)) if input_info in file_ids else input_info

        for length_label, length in length_tests.items():
            # Use only a portion of the text based on the length label
            test_text = raw_text[:length]

            # Convert text to bytes
            byte_sequence = text_to_bytes(test_text)

            # Run tests for Standard and optionally for Compact Trie
            for trie_type in ["Standard", "Compact"]:
                if trie_type == "Compact" and not use_compact:
                    continue  # Skip if --compact is not set

                use_compact_trie = trie_type == "Compact"

                # Step 1: Compress the Byte Sequence Using LZW
                compressor = LZWCompressor(max_bits=max_bits, use_compact_trie=use_compact_trie, fixedLZW=fixed_lzw)
                compressed_data, compress_stats = compressor.compress(byte_sequence, generate_stats=True)
                compress_stats['trie_type'] = trie_type
                compress_stats['text_length'] = length_label.split(' ')[0]
                compress_stats['file_id'] = os.path.basename(file_id).split('.')[0] if args.file else file_id

                # Store compression statistics
                all_stats.append(compress_stats)

                # Step 2: Decompress the Data Using LZW
                decompressor = LZWDecompressor(max_bits=max_bits, fixedLZW=fixed_lzw)
                decompressed_bytes, decompress_stats = decompressor.decompress(compressed_data[:], generate_stats=True)  # Use a copy of compressed_data
                decompress_stats['trie_type'] = trie_type
                decompress_stats['text_length'] = length_label.split(' ')[0]
                decompress_stats['file_id'] = os.path.basename(file_id).split('.')[0] if args.file else file_id

                # Store decompression statistics
                all_stats.append(decompress_stats)

                # Convert decompressed bytes back to text
                decompressed_text = bytes_to_text(decompressed_bytes)

                # Step 3: Verify if the decompressed text matches the original text
                if test_text == decompressed_text:
                    print(f"SUCCESS\t{trie_type:<10}{length_label.split(' ')[0]:<10}{file_id}")
                else:
                    print(f"ERROR\t{trie_type}\t{length_label.split(' ')[0]}\t{file_id}")

    # Optionally, save statistics to a CSV file for further analysis
    if generate_stats:
        output_file = "stats.csv"
        with open(output_file, mode='w', newline='') as csv_file:
            fieldnames = ['operation', 'ratio', 'dictionary_size', 'memory_usage', 'execution_time', 'bits_used', 'trie_type', 'text_length', 'file_id']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for stat in all_stats:
                writer.writerow(stat)

        print(f"\nStatistics have been saved to {output_file}")

    # Optionally, generate graphs about results statistics
    if plot_graphs:
        generate_graphs(all_stats, output_folder=".")

if __name__ == "__main__":
    main()
