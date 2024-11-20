import matplotlib.pyplot as plt
import pandas as pd

def generate_graphs(all_stats, output_folder="."):
    # Convert all_stats to a DataFrame
    stats_df = pd.DataFrame(all_stats)

    # Ensure there are no empty values in the DataFrame
    stats_df.dropna(inplace=True)

    # Map text_length categories to numerical values for easier plotting
    text_length_mapping = {
        'Short': 1,
        'Medium': 2,
        'Long': 3,
        'Huge': 4
    }
    stats_df['text_length_numeric'] = stats_df['text_length'].map(text_length_mapping)

    # Filter data into compression and decompression stats
    compression_stats = stats_df[stats_df['operation'] == 'compression']
    decompression_stats = stats_df[stats_df['operation'] == 'decompression']

    # Set constants for plotting
    width, height = 8, 4
    linewidth = 4
    zorder = 3
    text_length_labels = ['< 100', '100 - 1000', '1000 - 10000', '10000 - 100000']
    text_length_ticks = [1, 2, 3, 4]

    # Graph 1: Compression Ratio Comparison
    def plot_compression_ratio():
        plt.figure(figsize=(width, height))
        grouped_data = compression_stats.groupby(['file_id', 'trie_type'])
        for (file_id, trie_type), group in grouped_data:
            group = group.sort_values(by='text_length_numeric')
            color = '#1f77b4' if trie_type == "Standard" else '#ff7f0e'
            linestyle = '-' if trie_type == "Standard" else '--'
            plt.plot(group['text_length_numeric'], group['ratio'],
                     linestyle=linestyle, color=color,
                     linewidth=linewidth, alpha=0.5)
            plt.scatter(group['text_length_numeric'], group['ratio'],
                        marker='o' if trie_type == "Standard" else 's', color=color,
                        s=100, zorder=zorder)
        plt.plot([], [], color='#1f77b4', linestyle='-', linewidth=linewidth, label='Standard Trie')
        plt.plot([], [], color='#ff7f0e', linestyle='--', linewidth=linewidth, label='Compact Trie')
        plt.xlabel('Text Length Category')
        plt.ylabel('Compression Ratio')
        plt.title('Compression Ratio Comparison')
        plt.xticks(ticks=text_length_ticks, labels=text_length_labels)
        plt.grid(True)
        plt.tight_layout()
        plt.legend()
        plt.savefig(f"{output_folder}/compression_ratio.png")
        plt.close()

    # Graph 2: Memory Usage Comparison
    def plot_memory_usage():
        plt.figure(figsize=(width, height))
        grouped_data = compression_stats.groupby(['file_id', 'trie_type'])
        for (file_id, trie_type), group in grouped_data:
            group = group.sort_values(by='text_length_numeric')
            color = '#d62728' if trie_type == "Standard" else '#17becf'
            linestyle = '-' if trie_type == "Standard" else '--'
            plt.plot(group['text_length_numeric'], group['memory_usage'],
                     linestyle=linestyle, color=color,
                     linewidth=linewidth, alpha=0.5)
            plt.scatter(group['text_length_numeric'], group['memory_usage'],
                        marker='o' if trie_type == "Standard" else 's', color=color,
                        s=100, zorder=zorder)
        plt.plot([], [], color='#d62728', linestyle='-', linewidth=linewidth, label='Standard Trie')
        plt.plot([], [], color='#17becf', linestyle='--', linewidth=linewidth, label='Compact Trie')
        plt.xlabel('Text Length Category')
        plt.ylabel('Memory Usage (Bytes)')
        plt.title('Memory Usage Comparison')
        plt.xticks(ticks=text_length_ticks, labels=text_length_labels)
        plt.grid(True)
        plt.tight_layout()
        plt.legend()
        plt.savefig(f"{output_folder}/memory_usage.png")
        plt.close()

    # Graph 3: Execution Time Comparison (Compression)
    def plot_execution_time_compression():
        plt.figure(figsize=(width, height))
        grouped_data = compression_stats.groupby(['file_id', 'trie_type'])
        for (file_id, trie_type), group in grouped_data:
            group = group.sort_values(by='text_length_numeric')
            color = 'c' if trie_type == "Standard" else 'orange'
            linestyle = '-' if trie_type == "Standard" else '--'
            plt.plot(group['text_length_numeric'], group['execution_time'],
                     linestyle=linestyle, color=color,
                     linewidth=linewidth, alpha=0.5)
            plt.scatter(group['text_length_numeric'], group['execution_time'],
                        marker='^' if trie_type == "Standard" else 'v', color=color,
                        s=100, zorder=zorder)
        plt.plot([], [], color='c', linestyle='-', linewidth=linewidth, label='Standard Trie')
        plt.plot([], [], color='orange', linestyle='--', linewidth=linewidth, label='Compact Trie')
        plt.xlabel('Text Length Category')
        plt.ylabel('Execution Time (Seconds)')
        plt.title('Compression Time')
        plt.xticks(ticks=text_length_ticks, labels=text_length_labels)
        plt.grid(True)
        plt.tight_layout()
        plt.legend()
        plt.savefig(f"{output_folder}/compression_time.png")
        plt.close()

    # Graph 4: Execution Time Comparison (Decompression)
    def plot_execution_time_decompression():
        plt.figure(figsize=(width, height))
        grouped_data = decompression_stats.groupby(['file_id', 'trie_type'])
        for (file_id, trie_type), group in grouped_data:
            group = group.sort_values(by='text_length_numeric')
            color = 'y' if trie_type == "Standard" else 'k'
            linestyle = '-' if trie_type == "Standard" else '--'
            plt.plot(group['text_length_numeric'], group['execution_time'],
                     linestyle=linestyle, color=color,
                     linewidth=linewidth, alpha=0.5)
            plt.scatter(group['text_length_numeric'], group['execution_time'],
                        marker='d' if trie_type == "Standard" else '*', color=color,
                        s=100, zorder=zorder)
        plt.plot([], [], color='y', linestyle='-', linewidth=linewidth, label='Standard Trie')
        plt.plot([], [], color='k', linestyle='--', linewidth=linewidth, label='Compact Trie')
        plt.xlabel('Text Length Category')
        plt.ylabel('Execution Time (Seconds)')
        plt.title('Decompression Time')
        plt.xticks(ticks=text_length_ticks, labels=text_length_labels)
        plt.grid(True)
        plt.tight_layout()
        plt.legend()
        plt.savefig(f"{output_folder}/decompression_time.png")
        plt.close()

    # Graph 5: Dictionary Size Comparison
    def plot_dictionary_size():
        plt.figure(figsize=(width, height))
        grouped_data = compression_stats.groupby(['file_id', 'trie_type'])
        for (file_id, trie_type), group in grouped_data:
            group = group.sort_values(by='text_length_numeric')
            color = 'orange' if trie_type == "Standard" else 'g'
            linestyle = '-' if trie_type == "Standard" else '--'
            plt.plot(group['text_length_numeric'], group['dictionary_size'],
                     linestyle=linestyle, color=color,
                     linewidth=linewidth, alpha=0.5)
            plt.scatter(group['text_length_numeric'], group['dictionary_size'],
                        marker='p' if trie_type == "Standard" else 'h', color=color,
                        s=100, zorder=zorder)
        plt.plot([], [], color='orange', linestyle='-', linewidth=linewidth, label='Standard Trie')
        plt.plot([], [], color='g', linestyle='--', linewidth=linewidth, label='Compact Trie')
        plt.xlabel('Text Length Category')
        plt.ylabel('Dictionary Size')
        plt.title('Dictionary Size Growth')
        plt.xticks(ticks=text_length_ticks, labels=text_length_labels)
        plt.grid(True)
        plt.tight_layout()
        plt.legend()
        plt.savefig(f"{output_folder}/dictionary_size_growth.png")
        plt.close()

    # Run the plotting functions to generate the graphs
    plot_compression_ratio()
    plot_memory_usage()
    plot_execution_time_compression()
    plot_execution_time_decompression()
    plot_dictionary_size()
