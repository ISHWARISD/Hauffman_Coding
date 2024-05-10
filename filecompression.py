import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import heapq
import collections
import os

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = collections.Counter(text)
    heap = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def build_huffman_codes(node, prefix="", codes={}):
    if node is not None:
        if node.char is not None:
            codes[node.char] = prefix
        build_huffman_codes(node.left, prefix + "0", codes)
        build_huffman_codes(node.right, prefix + "1", codes)
    return codes

def encode_text(text, codes):
    encoded_text = ""
    for char in text:
        encoded_text += codes[char]
    return encoded_text

def compress(text):
    huffman_tree = build_huffman_tree(text)
    huffman_codes = build_huffman_codes(huffman_tree)
    encoded_text = encode_text(text, huffman_codes)
    
    initial_size = len(text.encode('utf-8'))
    compressed_size = (len(encoded_text) + 7) // 8
    compression_ratio = (compressed_size / initial_size) * 100

    return huffman_codes, initial_size, compressed_size, compression_ratio

def compress_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        messagebox.showerror("Error", "Please select a text file.")
        return

    with open(file_path, "r") as file:
        text = file.read()

    huffman_codes, initial_size, compressed_size, compression_ratio = compress(text)
    
    codes_text.delete("1.0", "end")
    for char, code in huffman_codes.items():
        codes_text.insert("end", f"{char}: {code}\n")

    initial_size_label.config(text=f"Initial size: {initial_size} bytes")
    compressed_size_label.config(text=f"Compressed size: {compressed_size} bytes")
    compression_ratio_label.config(text=f"Compression ratio: {compression_ratio:.2f}%")

# Create the main window
root = tk.Tk()
root.title("Huffman Coding Compression")

# Create and configure input frame
input_frame = ttk.Frame(root, padding="20")
input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

compress_button = ttk.Button(input_frame, text="Select File", command=compress_file)
compress_button.grid(row=0, column=0, pady=5)

# Create and configure output frame
output_frame = ttk.Frame(root, padding="20")
output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

codes_label = ttk.Label(output_frame, text="Huffman Codes:")
codes_label.grid(row=0, column=0, sticky=(tk.W, tk.N))

codes_text = tk.Text(output_frame, height=5, width=50)
codes_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

initial_size_label = ttk.Label(output_frame, text="")
initial_size_label.grid(row=2, column=0, sticky=(tk.W, tk.N))

compressed_size_label = ttk.Label(output_frame, text="")
compressed_size_label.grid(row=3, column=0, sticky=(tk.W, tk.N))

compression_ratio_label = ttk.Label(output_frame, text="")
compression_ratio_label.grid(row=4, column=0, sticky=(tk.W, tk.N))

root.mainloop()
