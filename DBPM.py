import heapq
from collections import defaultdict, Counter

# Node class for Huffman tree
class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char    # Character/byte
        self.freq = freq    # Frequency of the character/byte
        self.left = left    # Left child ('0')
        self.right = right  # Right child ('1')

    def __lt__(self, other):
        return self.freq < other.freq

# Build Huffman tree based on byte frequency
def build_huffman_tree(frequencies):
    heap = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(left=left, right=right, freq=left.freq + right.freq)
        heapq.heappush(heap, merged)

    return heap[0]  # Root of the tree

# Generate Huffman codes by traversing the tree
def generate_huffman_codes(node, prefix='', code_map=None):
    if code_map is None:
        code_map = {}
    if node.char is not None:
        code_map[node.char] = prefix
    else:
        generate_huffman_codes(node.left, prefix + '0', code_map)
        generate_huffman_codes(node.right, prefix + '1', code_map)
    return code_map

# Convert binary string to bytes
def binary_string_to_bytes(binary_str):
    byte_array = bytearray()
    for i in range(0, len(binary_str), 8):
        byte_array.append(int(binary_str[i:i+8], 2))
    return bytes(byte_array)

# Convert bytes to binary string
def bytes_to_binary_string(byte_data):
    return ''.join(f'{byte:08b}' for byte in byte_data)

# Huffman compression
def huffman_compress(data):
    # Step 1: Calculate frequencies
    frequencies = Counter(data)

    # Step 2: Build Huffman tree
    root = build_huffman_tree(frequencies)

    # Step 3: Generate Huffman codes
    huffman_codes = generate_huffman_codes(root)

    # Step 4: Compress the data using Huffman codes
    binary_string = ''.join(huffman_codes[byte] for byte in data)

    # Convert binary string to bytes
    compressed_data = binary_string_to_bytes(binary_string)

    return compressed_data, huffman_codes

# Huffman decompression
def huffman_decompress(compressed_data, huffman_codes):
    # Reverse the Huffman code map
    reverse_code_map = {v: k for k, v in huffman_codes.items()}

    # Convert bytes back to binary string
    binary_string = bytes_to_binary_string(compressed_data)

    # Decode the binary string back to original data
    decoded_data = []
    buffer = ''
    for bit in binary_string:
        buffer += bit
        if buffer in reverse_code_map:
            decoded_data.append(reverse_code_map[buffer])
            buffer = ''

    return bytes(decoded_data)


def remove_marker_with_corruption(decompressed_data):
    # Define the marker
    marker = b"[0DBPM_COMPRESSOR_END0]" if isinstance(decompressed_data, bytes) else "[0DBPM_COMPRESSOR_END0]"
    marker_length = len(marker)
    
    # Define a threshold for the maximum corruption allowed (in this case, 2 characters)
    corruption_threshold = 5
    
    # Iterate through the data to find potential markers
    for i in range(len(decompressed_data) - marker_length + 1):
        # Extract the substring that might be the marker
        substring = decompressed_data[i:i + marker_length]
        
        # Check if the start of the substring matches the marker
        if isinstance(decompressed_data, bytes):
            if substring.startswith(marker[:-corruption_threshold]):
                # If we have a match with possible corruption, remove the marker
                return decompressed_data[:i]
        else:
            if substring.startswith(marker[:-corruption_threshold]):
                # If we have a match with possible corruption, remove the marker
                return decompressed_data[:i]
    
    # If no marker is found, return the original data
    return decompressed_data
