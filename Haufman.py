import heapq
import collections

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

def main():
    text = input("Enter the text string: ")

    # Compression
    huffman_tree = build_huffman_tree(text)
    huffman_codes = build_huffman_codes(huffman_tree)
    encoded_text = encode_text(text, huffman_codes)

    # Display Huffman codes
    print("Huffman Codes:")
    for char, code in huffman_codes.items():
        print(f"{char}: {code}")

    # Display initial size of text
    initial_size = len(text.encode('utf-8'))
    print(f"Initial size of text: {initial_size} bytes")

    # Calculate encoded size
    encoded_size = (len(encoded_text) + 7) // 8  # Round up to nearest byte
    print(f"Compressed size: {encoded_size} bytes")

    # Calculate compression ratio
    compression_ratio = (encoded_size / initial_size) * 100
    print(f"Compression ratio: {compression_ratio:.2f}%")

    print("Text compressed successfully.")

if __name__ == "__main__":
    main()
