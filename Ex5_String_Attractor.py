''' LAB EXERCISE:
STEP 1: 
Write a program that, given a string T and a set Γ of positions, check if Γ is a string attractor for T.
Moreover, find a string attractor for a given text T, by using the partition LZ77 and the BWT.

STEP 2:
Let us consider the finite Sturmian words. 
One can prove that finite Sturmian words have as smallest string attractor two consecutive positions. 
Verify if there exist other binary strings with the same length having the same property.

STEP 3:
Given the set of binary strings of length n, find how many and which ones have a minimum attractor of size 2.
'''
from Ex4_LZ_Family_BWT import encoding_LZ77, burrows_wheeler, set_T, set_W
import random

# ---
# Check that every substring located between positions if set_of_positions has an occurrence
# that intersects a position of the attractor.
def find_intersections( text : str, set_of_positions : list, sub_strings : list ):
    '''
    This function finds all the intersections of a list of substrings with the positions of an hypthetical string attractor.
    Input:
        - text : text, word or string from which we extract the substrings
        - set_of_positions: set containing the indexes that are the positions of the hypothetical string attractor
        - sub_strings: list of substrings to verify intersections
    
    Output:
        - True if all the substrings as an occurrence that intersects a position of the attractor
        - False if there exists a substring which occurrence do not intersect any postion of the attractor
    '''

    intersections = []              # List used to track how many intersections the substrings have
    for sub in sub_strings:
        
        # Step1: find all the occurrences taking all the indeces
        indices = []
        i = 0
        while i < len(text):
            index = text.find(sub, i)
            # Break the loop when there is no occurrence
            if index == -1:
                break
            
            indices.append(index)
            i = index + 1
        
        # Step2: find the intersections in the attractor - for each substrings, it counts how many intersections has
        count = 0
        for j in indices:
            for t in range(j, j + len(sub)):
                if t+1 in set_of_positions:
                    count += 1
        intersections.append((sub, count))
    
    # Step3: check if all the substrings have an intersection
    # If there is an intersection, this means that each substring has AT LEAST one occurrence over a position of the attractor.
    for i in range(len(intersections)):
        if intersections[i][1] == 0:
            return False
        elif intersections[i][1] != 0 and i == len(intersections)-1:
            return True

def string_attractor( text: str, set_of_positions: set ):
    '''
    This function verify if a given set of positions is a string attractor for a given string/text.
    Input:
        - text = string or text 
        - set_of_position = set containing the positions 
    
    Output: 
        - True if the set is a string attractor
        - False if the set is not a string attractor 
    '''
    set_of_positions = sorted(list(set_of_positions))       # Casting list over the set in order to access in an increasing order
    
    # List used to take track for each group of substrings to check if each substring intersects a position of the attractor: list of Trues/Falses
    intersections = []                                      

    # Determine all the substrings between positions: empty strings are considered
    for val in range(len(set_of_positions)):
        pos = set_of_positions[val]
        substrings = []
    
        # Check if the first position is the first character of the string
        # and determine the substrings from the beginning to the position.
        # Then determine all the substrings between the current position and the next one
        if pos != 1 and val == 0:
            substrings = [ text[i:j] for i in range( pos-1 ) for j in range( i+1, pos ) ]
            check = find_intersections(text, set_of_positions, substrings)
            intersections.append(check)
                        
            substrings.clear()
            substrings = [ text[i:j] for i in range( set_of_positions[val], set_of_positions[val+1] + 1 ) for j in range( i+1, set_of_positions[val+1]) ]
            check = find_intersections(text, set_of_positions, substrings)
            intersections.append(check)
        
        # Check if the last position is the last character of the string
        # and determine the substrings from the last position to the end of the string.
        elif val == len(set_of_positions)-1:
            substrings = [ text[i:j] for i in range( pos, len(text) + 1 ) for j in range( i+1, len(text) + 1 ) ]
            check = find_intersections(text, set_of_positions, substrings)
            intersections.append(check)
        else:
            substrings = [ text[i:j] for i in range( set_of_positions[val], set_of_positions[val+1] + 1 ) for j in range( i+1, set_of_positions[val+1] ) ]
            check = find_intersections(text, set_of_positions, substrings)
            intersections.append(check)
    
    if False in intersections:
        return False
    else:
        return True

# Functions to determine a string attractor using the partition of LZ77
def lz77_string_attractor( text : str, W : int ):
    '''
    Function that finds a string attractor using the LZ77 encoding of the text.
    Input:
        - text : text/string 
        - W : width of the window for the LZ77 encoding
    Output:
        - set of positions that is a string attractor for the given text: list
        - None if the set of position found is not a string attractor
    '''

    # Collecting the lengths of the phrases of the LZ77 encoding
    triples = encoding_LZ77(text, W)
    lengths = [ item[1] for item in triples ]

    # Determining the positions on the text based on the lenghts considered
    positions = []
    i = 0
    for l in lengths:
        i += l
        if i + 1 < len(text):
            positions.append(i+1)
            i += 1 
        else:
            break
    
    attractor = string_attractor(text, positions)
    if attractor:
        return positions
    else:
        return None

def bwt_string_attractor( text : str ):
    '''
    Function that finds a string attractor using the Burrows-Wheeler Transform of the text.
    Input:
        - text: text/string 
    Output:
        - positions: set of positions that is a string attractor for the text: list
        - None if the set found is not a string attractor
    '''

    # Determining from the BWT(text) which are the characters of the texts that are positions of the attractor.
    # Create a list of tuples (chr, pos, '*') that is the column L in which it keep track
    # of the position and if the character is important or not.
    bwt, I = burrows_wheeler(text)

    # The characters to search for their position in the original text, are the ones 
    # which represents the first character of each equal-letter run of the BWT
    indices = []
    i = 0
    while i != len(bwt)-1 and i < len(bwt):
        for j in range(i+1, len(bwt)):
            if bwt[j] != bwt[j-1]:
                indices.append(i)
                break
        i = j
    if i == len(bwt) - 1:
        indices.append(i)
    
    L = [ ( bwt[i], i, '*' if i in indices else None) for i in range(len(bwt)) ]          # Column L characterized by the first character of the runs

    # Determining the list F, first column of the lexicographic sorting 
    # of the cyclic rotations: it has tuples such ( L[i], j )
    F = sorted(L, key = lambda x: x[0])

    # Determining the permutation to use to obtain the original word: it uses the indices of L and F
    t = [I]
    pos = I
    while True:
        t.append(F[pos][1])
        pos = F[pos][1]
        
        if pos == I:
            t = t[: len(t)-1]
            break
    
    # Determining the positions starting from the permutation and F
    original_text = [ F[i] for i in t ]
    positions = [ pos  for pos in range(len(original_text)) if original_text[pos][2] == '*' ]

    attractor = string_attractor(text, positions)
    if attractor:
        return positions
    else:
        return None

# ---
# In order to verify STEP2, there will be used the sets of binary words used in Ex.4

# Finite Sturmian Words implementation
def Sturmian_words( sequence : list ):
    '''
    Function that generete a list containing all the Finite Sturminian words, starting from a sequence of natural numbers.
    Input:
        - sequence : n natural numbers, (d_1, ..., d_n), d_1>=0
    Output:
        - Sturmian words : list containing all the words
    '''
    sturmian_words = ['b', 'a']
    i = 1 
    for num in sequence:
        sturmian_words.append( num * sturmian_words[i] + sturmian_words[i-1] )
        i += 1
    
    return sturmian_words

def minimal_string_attractor( words_set : list ):
    '''
    Function that verify if a set of words has as minimal string attractor of size 2 with 2 consecutive positions.
    It uses the LZ77 parsing.
    Input:
        - words_set: list of words to check
    Output:
        - list of tuples: (word, positions, len(word))
        - None: no minimal string attractor of size 2 found
    '''
    minimal_SA = []
    for word in words_set:
        attractor_LZ77 = lz77_string_attractor(word, 16)
        if attractor_LZ77:
            # For each position, create two sets of two positions: one with the previous and one with the next position
            # and verify if it is a string attractor, printing also the lenght of the word.
            min_attractors = [] 
            for pos in attractor_LZ77:
                if pos == 1:
                    cons_positions = [pos, pos+1]
                    attractor = string_attractor(word, cons_positions)
                    if attractor:
                        min_attractors.append(cons_positions)
                
                elif pos == len(word):
                    cons_positions = [pos-1, pos]
                    attractor = string_attractor(word, cons_positions)
                    if attractor:
                        min_attractors.append(cons_positions)
                
                elif pos != 1 and pos != len(word):
                    cons_positions_1 = [pos-1, pos]
                    attractor_1 = string_attractor(word, cons_positions_1)
                    if attractor_1:
                        min_attractors.append(cons_positions_1)
                    
                    cons_positions_2 = [pos, pos+1]
                    attractor_2 = string_attractor(word, cons_positions_2)
                    if attractor_2:
                        min_attractors.append(cons_positions_2)
            if min_attractors:
                minimal_SA.append((word, min_attractors,len(word)))
    
    if minimal_SA:
        return minimal_SA
    else:
        None  

# ---
# Set of binary strings of length n
def binary_strings( n : int):
    '''
    Set representin the binary strings of length n.
    Input:
        - n: length of the words
    Output:
        - list containing the words
    '''
    if n == 0:
        return ['']
    
    strings = binary_strings(n - 1)
    return [s + '0' for s in strings] + [s + '1' for s in strings]


if __name__ == '__main__':
    print(" STRING ATTRACTOR ")
    print(" What do you want to do? ")
    print("a. Verify if a set is a string attractor of a text/string + find a string attractor by using LZ77 and BWT.")
    print("b. Results/analysis of step 2: Sturmian words and minimal attractor.")
    print("c. Binary strings: attractor of size 2 - numbers.")
    ans = str(input())

    while ( ans not in ('a', 'A', 'b', 'B', 'c', 'C')):
        ans = str(input("Please try again... "))
    
    if ans in ('a', 'A'):
        T = str(input("Insert the string/text: "))
        P = set()                                      # Set containing the positions to verify as String Attractor
        print("Insert the positions to verify:")
        while True:
            pos = input()
            if pos == '':
                break
            elif pos.isdigit():                         # Verify if the user insert an integer               
                P.add(int(pos))
            else:
                print("Try again...")
                continue
        
        # Check if the candidate as string attractor satisfies the inequality in respect to the cardinality of the alphabet:
        # |string attractor| >= |alphabet|
        A = set(T) # Alphabet set of the string inserted
        if len(P) >= len(A):
            print("The set of positions inserted satisfies the inequality.")
        else:
            print("The set of positions inserted does not satisfy the inequality.")
        
        # Verify if the set S is a string attractor
        attractor = string_attractor(T, P)
        if attractor:
            print(f"This set {P} is a string attractor.")
        else:
            print(f"This set {P} is not a string attractor.")

        # Determine a string attractor using partition of LZ77 and BWT
        print("-------")
        W = random.randint(5, 16)
        attractor_lz77 = lz77_string_attractor(T,W)
        if attractor_lz77 != None:
            print(f"A string attractor using LZ77 is {attractor_lz77}.")
        else:
            print("No string attractor found using LZ77 phrases.") 
           
        print("-------")
        attractor_bwt = bwt_string_attractor(T)
        if attractor_bwt != None:
            print(f"A string attractor usign BWT is {attractor_bwt}")
        else:
            print("No string attractor found using BWT.")
    
    elif ans in ('b', 'B'):
        
        # ---
        # Generate randomly set of binary words of the set Set_T: ab^(j^k)
        k = random.randint(2,5)
        i = random.randint(2,5)
        words_T = set_T(k,i)
        minimal_attractors = minimal_string_attractor(words_T)
        print(f"Considering the set of binary words {words_T}:")
        if minimal_attractors:
            for el in minimal_attractors:
                print(f"The word {el[0]} has as minimal attractor of size 2:")
                for sets in el[1]:
                    print(f" {sets} with length {el[2]}")
        else:
            print(f"The words have not minimal string attractor of size 2.")
        
        print()
        print("-----")
        print()


        # ---
        # Generate randomly the set of binary words of the set W: ((ab^iaa)(ab^iaba^(i-2)))ab^ka, k>5 and i = 2,_,k-1
        k = random.randint(6, 9)
        words_W = set_W(k)
        minimal_attractors = minimal_string_attractor(words_W)
        print(f"Considering the set of binary words {words_W}:")
        if minimal_attractors:
            for el in minimal_attractors:
                print(f"The word {el[0]} has as minimal attractor of size 2:")
                for sets in el[1]:
                    print(f" {sets} with length {el[2]}")
        else:
            print(f"The words have not minimal string attractor of size 2.")
    
    elif ans in ('c', 'B'):
        n = int(input("Insert the length of the binary words to analyse: "))
        while n <= 0:
            n = int(input("Please, try again..."))
        print()
        words_binary = binary_strings(n)
        attractor_binary = minimal_string_attractor(words_binary)
        if attractor_binary:
            print(f"The following {len(attractor_binary)} has minimal string attractor of size 2:")
            for el in attractor_binary:
                print(f" {el[0]} has string attractor ", end = '')
                for elm in el[1]:
                    print(elm, end = '')
                print()