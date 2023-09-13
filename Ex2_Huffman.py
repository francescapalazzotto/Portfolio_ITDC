''' LAB EXERCISE:
Given an input text, find the Huffman encoding of the text.

A decoding procedure to recover the original message by starting from the Huffman encoding
is also required.
'''

import re

# Defining a class for the leaves of the Huffman tree:
#   - s is the symbol
#   - p is the probability of s
class Leaves:
    def __init__(self, s, p, sx = None, dx = None):
        self.s = s
        self.p = p
        self.sx = sx
        self.dx = dx
    
    def __repr__(self):
        return f"Leave({self.s}, {self.p})"

# Defining a class for the nodes
class Node:
    def __init__(self, s, p, sx = None, dx = None):
        self.s = s          # Symbol
        self.p = p          # Probability
        self.sx = sx        # Left child
        self.dx = dx        # Right child
    
# Defining a recursive function that traverse the Huffman tree and construct the dictionary of codewords
def binary_code_Huffman(root : object , codeword = ''):
    '''
    Recursive function that created the dictionary of codewords
    Input:
        - root of the Huffman tree
        - codeword = '' starts with the empty codeword
    Output:
        - dictionary of codewords
    '''
    codewords = {}

    def tree_visit(node : object, codeword):
        if node is not None:
            # Verify if the current node is a leaf and add the codeword to the dictionary
            if node.sx is None and node.dx is None:
                codewords[node.s] = codeword
            # Recursive calls to the left and right child
            else:
                tree_visit(node.sx, codeword + '0')
                tree_visit(node.dx, codeword + '1')
    
    # Starts the visit
    tree_visit(root, codeword)

    return codewords


def encoding_Huffman(text : str):
    '''
    Function that creates the encoding of the text using the Huffman algorithm using binary codes.
    Input:
        - text : string/text to encode
    Output:
        - text encoded
        - dictionary of codewords
    '''
    # Scanning the whole text and counting each different symbol - using a list of tuples ( a, occ(a) ) where a is a symbol
    text_symbols = list(set(text))
    occurrences = [ ( el, len( re.findall(el, text) ) ) for el in text_symbols ]

    # Determining the probability of each symbols based of its occurrences - using a list of tuples ( a, p_a ) where p_a = occ(a)/len(text)
    t = len(text)
    probabilities = [ ( item[0], round( item[1]/t , 2 ) ) for item in occurrences ]

    # Sorting the probabilities in a increasing order - this because it is needed 
    # that the first node in the queue must be the one with the smallest probability
    probabilities = sorted(probabilities, key = lambda x: x[1])

    # Generates leaves nodes for each symbol containing the respective probabilities and add them to the queue
    queue = [ Leaves( el[0], el[1] ) for el in probabilities ]

    # While loop to construct the Huffman tree:
    while len(queue) > 1:
        # Dequeue two nodes 
        s = queue.pop()
        t = queue.pop()
        # Create a new node with probability the sum of the previous
        p = round(s.p + t.p, 2) 
        symbol = ( s.s + ',' + t.s )
        u = Node(symbol, p)
        u.dx = s
        u.sx = t

        # Enqueue the new node
        queue.insert(0, u)
    root = queue.pop()

    # Construction of the dictionary containing the codewords
    dict_codewords = binary_code_Huffman(root)

    # Encoding the text using the codewords
    encoded_text = ''
    for symbol in text:
        encoded_text += dict_codewords[symbol]
    
    return encoded_text, dict_codewords

def decoding_Huffman(encoded_text : str, codewords : dict):
    '''
    Function that decode a text using a dictionary of codewords created by Huffman encoding.
    Input:
        - encoded text
        - codewords: dictionary that contains all the symbols and codewords
    Output:
        - decoded text
    '''

    decoded_text = ''
    # Create an inverse dictionary to access rapidly to codewords
    dictionary = { codeword : symbol for symbol, codeword in codewords.items() }
    codewords_1 = list(dictionary)        # Obtaining a list of the keys from the dictionary

    # Traverse the encoded text and looking for codewords in the list
    i = 0
    while i < len(encoded_text):
        for j in range(i+1, len(encoded_text)+1):
            if encoded_text[i:j] in codewords_1:
                decoded_text += dictionary[ encoded_text[i:j] ]
                break
        i = j

    return decoded_text 





if __name__ == '__main__':
    print("HUFFMAN ENCODING ALGORITHM WITH BINARY CODES")
    print()
    text = str(input("Insert the text to compress: "))
    text_encoded, dictionary = encoding_Huffman(text)
    print()
    print(f"The Huffman encoding is {text_encoded}")
    print()
    print(f"Using the following codewords:")
    for key in dictionary.keys():
        print(f" {key} -> {dictionary[key]}")
    
    print("---")
    print("The decoding phase is implemented too, obtaining:")
    text_decoded = decoding_Huffman(text_encoded, dictionary)
    print(f"{text_decoded}")