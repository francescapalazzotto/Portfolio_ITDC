''' LAB EXERCISE:
Write a program that given a text T, outputs the LZ77 encoding and the LZss encoding of the text.
A parameter of the program should be W, the length of the search buffer. 

Experiment 1: Compare the number of triplets denoted by z produced by LZ77(T) (or by LZss) and the number of the equal-letter
runs denoted by r produced by the BWT(T). Test esperimentally when such relations holds. 

Experiment 2: Text experimentally and computes these values for some binary words.
'''

from math import log2
from statistics import mean

# Function to determine the Burrows-Wheeler Transform of a text
def burrows_wheeler(word):
    '''
    This function calculates the Burrows-Wheeler Transform of a word or text
    Returns: 
        - L = last coloumn of the matrix containing all the cyclic rotations of the word/text
        - k = position of the original word in the cyclic rotations

    '''
    n = len(word)
    M = [word]                                      #Implemented list containing all the cyclic rotations of the word
    word_copy = word                                #Using a copy of the original word to construct all the cyclic rotations, in order to not change its value
    i = 1
    while i < n:
        rot = word_copy[1:] + word_copy[0]           #Rotation of the word
        M.append(rot)
        word_copy = rot
        i += 1
    
    M = sorted(M)                                    #Lexicographic order of the cyclic rotations
    L = ''                                           #Last coloumn of the matrix - the output
    for j in range(n):
        L += (M[j])[n-1]                             #Takes the last character of each rotation
    
    k = 0
    while k < n:
        if M[k] == word:
            break
        k += 1
    
    return L, k

# Defining a function to determin the equal-letter runs of BWT 
def equal_letter_runs(text):
    bwt, I = burrows_wheeler(text)
    r = 1
    for i in range(1, len(bwt)):
        if bwt[i] != bwt[i-1]:
            r += 1 
    return r

# Defining the LZ77 algorithm with a sliding window of width equals to W
def encoding_LZ77(text, W = 16):
    '''
    Encode a text using LZ77 algorithm - W is the width of the sliding window.
    Returns a list of triplets (o,l,s):
        - o is the offset
        - l is the prefix (phrase)
        - s is the symbol appearing on the look-ahead buffer after the prefix
    '''
    compressed_text = []                    # List of triplets
    search_buffer = ""
    i = 0                                   # Pointer used to slide the look-ahead buffer 
    
    while i < len(text):
        # Find the longest match in the search buffer
        longest_match = ""
        offset = 0
        length = 0

        for j in range(1, min(len(search_buffer)+1, W+1)):
            if text[i:i+j] in search_buffer:
                longest_match = text[i:i+j]
                length = len(longest_match)
                offset = len(search_buffer) - search_buffer.index(longest_match)
        
        # Appending the triplets in the compressed text to be returned
        if longest_match:
            symbol = text[i+length] if i+length < len(text) else None
            compressed_text.append((offset, length, symbol))
            i += length + 1
        else:
            compressed_text.append((0, 0, text[i]))
            i += 1
        
        search_buffer = text[max(0, i-W):i]
    
    return compressed_text

# Defining the LZss algorithm with a sliding window of width equals to W
def encoding_LZss(text, W):
    '''
    This algorithm is a variant of LZ77 algorithm. 
    It takes as input the text to be compressed and returns a list of couples:
        - (d, |a|): d is distance and a is the prefix, |a| is the length of the prefix.
        - (0, c): means that it inserts a new symbol: distance is 0 and c is the symbol to insert.
    '''
    compressed_text = []                            # List of couples of the text compressed
    search_buffer = ""
    i = 0                                           # Pointer used to slide the look-ahead buffer 

    while i < len(text):
        # Find the prefix in the search buffer
        prefix = ""
        distance = 0
        
        for j in range(1, min(len(search_buffer)+1, W+1)):
            if text[i:i+j] in search_buffer:
                prefix = text[i:i+j]
                distance = search_buffer.index(prefix) + 1
        
        # Appending the couples in the compressed text to be returned
        if prefix:
            compressed_text.append((distance, len(prefix)))
            i += len(prefix)
        else:
            symbol = text[i]
            compressed_text.append((0, symbol))
            i += 1
        
        search_buffer = text[max(0, i-W):i]
    
    return compressed_text

# Defining a function to test the Experiment 1 to determine results about the relations hold 
# based on the value of n = length of the text.
def experiment_1(text, W):
    '''
    In this function, the text is compressed using the LZ77 algorithm using a sliding window of width W.
    It returns a list containing couples ( N, True/False ) in which:
        - N is the length of the row of the text read.
        - True/False: it is True if the values z (triplets of LZ77) and r (equal-letters runs of BWT) of the text 
        hold the two relations, False otherwise. 
    ''' 
    relations = []
    for row in text.readlines():
        z = len(encoding_LZ77(row, W))
        r = equal_letter_runs(row)
        N = len(row)

        if r <= z*pow(log2(N), 2) and z <= r*log2(N):
            relations.append((N, True))
        else:
            relations.append((N, False))
    
    return relations 


# ---
# Defining the sets of binary words regarding the Experiment 2
# Set T_k
def set_T(k: int, i: int):
    '''
    Input:
        - k > 0
        - i >= 1
    Output:
        - list of binary words of the form ab^(j^k)
    '''
    words = []
    for j in range(1, i+1):
        w = "a" + (j**k) * "b"
        words.append(w)
    
    return words

# Set Fibonacci words of odd and even order.
def odd_even_Fibonacci(n: int):
    '''
    Input:
        - The parameter n used is referred to the total number of the set that we want to compress
    Output:
        - list of first n odd Fibonacci numbers
        - list of first n even Fibonacci numbers
    '''
    words_odd = ["a"]
    words_even = ["b"]
    fib_words = ["a", "b"]

    for i in range(2, 2*n):
        fib = fib_words[i-1] + fib_words[i-2]
        fib_words.append(fib)
        if i % 2 == 0:
            words_even.append(fib)
        else:
            words_odd.append(fib)
    
    return words_odd, words_even

#Set W_k
def set_W(k: int):
    '''
    Input:
        - k > 5
    Output:
        - list of binary words
    '''
    words = []

    for i in range(2, k):
        s = "a" + i*"b" + "aa"
        e = "a" + i*"b" + "ab" + (i-2)*"a"
        q = "a" + k*"b" + "a"
        words.append(s+e+q)
    
    return words


if __name__ == '__main__':
    print("LZ Family algorithms: LZ77 and LZss - BWT")
    print()
    print("What do you want to see?")
    print("a. Encoding of a text T.")
    print("b. Results for Experiment 1. ")
    print("c. Results for Experiment 2. ")
    ans = str(input())

    while ( ans not in ('a', 'A', 'b', 'B', 'c', 'C') ):
        ans = str(input("Please, try again ... "))

    if ans in ('a', 'A'):
        print("Insert the text you want to encode:")
        text = str(input())
        print("How wide should the sliding window be?")
        W = int(input())
        compressed_LZ77 = encoding_LZ77(text, W)
        compressed_LZss = encoding_LZss(text, W)
        print()
        print("The compressed text is:")
        print("- using LZ77 algorithm")
        for item in compressed_LZ77:
            print(item)
        print("- using LZss algorithm")
        for item in compressed_LZss:
            print(item)
    
    elif ans in ('b', 'B'):
        print("Results of Experiment 1 applying the LZ77 algorithm and Burrows-Wheeler Transform applied to the first 3 chapters of the Pride and Prejudice book.\nFor the sliding window, the width chosen to apply the LZ77 algorithm is equal to 7.")
        text =  open(r"C:\Users\palaz\OneDrive\Desktop\University\UNIPA 2.0\I ANNO\II semestre\ITDC - Information Theory and Data Compression\Palazzotto_Portfolio_ITDC\Pride and Prejudice - Ch. 1-2-3.txt")
        listed_relations = experiment_1(text, 7)

        # To analyze the results of the experiment, we count the number of times the relationships hold true 
        # and the corresponding range for the length of the corresponding row
        count = 0
        lengths = []
        for item in listed_relations:
            if item[1] == True:
                count += 1
                lengths.append(item[0])
        val = round(mean(lengths),2)
        print()
        print("There is a total of ", count, "True values with an average text length of ", val)
    
    elif ans in ('c', 'C'):
        print("Results of values z (triplets) and r (equal-letter runs) applied to binary words.")
        print("Insert the parameters:")
        
        print("- Set T: ")
        k = int(input("k = "))
        while (k < 0):
            k = int(input("Try again..."))
        
        t = int(input("i = "))
        while (t < 1):
            t = int(input("Try again..."))
        
        words_T = set_T(k, t)
        lz77_T = [ encoding_LZ77(word, 7) for word in words_T ]
        z_T = [ len(item) for item in lz77_T ]
        bwt_T = [ burrows_wheeler(word)[0] for word in words_T ]
        r_T = [ equal_letter_runs(item) for item in bwt_T ]

        print()
        print("The number of triplets of the LZ77 algorithm are")
        print(z_T)
        print("The number of equal-letter runs are")
        print(r_T)
        print()

        print("- Fibonacci words: ")
        n = int(input("n = "))
        while (n < 2):
            n = int(input("Try again..."))
        
        words_odd, words_even = odd_even_Fibonacci(n)
        lz77_odd = [ encoding_LZ77(word, 7) for word in words_odd ]
        z_odd = [ len(item) for item in lz77_odd ]
        bwt_odd = [ burrows_wheeler(word)[0] for word in words_odd ]
        r_odd = [ equal_letter_runs(item) for item in bwt_odd ]

        print()
        print("ODD ORDER")
        print("The number of triplets of the LZ77 algorithm are")
        print(z_odd)
        print("The number of equal-letter runs are")
        print(r_odd)

        lz77_even = [ encoding_LZ77(word, 7) for word in words_even ]
        z_even = [ len(item) for item in lz77_even ]
        bwt_even = [ burrows_wheeler(word)[0] for word in words_even ]
        r_even = [ equal_letter_runs(item) for item in bwt_even ]

        print()
        print("EVEN ORDER")
        print("The number of triplets of the LZ77 algorithm are")
        print(z_even)
        print("The number of equal-letter runs are")
        print(r_even)
        print()

        print("- Set W: ")
        x = int(input("k = "))
        while (x < 5):
            x = int(input("Try again..."))
        
        words_W = set_W(x)
        lz77_W = [ encoding_LZ77(word, 7) for word in words_W ]
        z_W = [ len(item) for item in lz77_W ]
        bwt_W = [ burrows_wheeler(word)[0] for word in words_W ]
        r_W = [ equal_letter_runs(item) for item in bwt_W ]

        print()
        print("The number of triplets of the LZ77 algorithm are")
        print(z_W)
        print("The number of equal-letter runs are")
        print(r_W)