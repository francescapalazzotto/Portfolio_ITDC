''' LAB EXERCISE: 
Write a program that, given a string T, construct the grammar produced by the algorithm RE-PAIR.

Implement also the construction of the grammar in the Chomsky normal form.

Compute also the size of the grammar in both cases. 

'''
import re

def re_pair( text : str ):
    '''
    RE-PAIR algorithm applied to the given string.
    Input:
        - text: string to compress 
    Output:
        - compressed text
        - dictionary: set of productions containing all the rules generated
    '''
    text = text.lower()
    # Using a while loop that breaks when all the frequencies are 1:
    # that means there is no need to create a new rule
    P = {}          # Dictionary of rules: set of productions
    new_symbol = chr(ord('A')-1)
    while True:
        
        # Calculate all the distinct pairs of symbols XY
        pairs = []
        for i in range(len(text)-2):
            pair = text[i:i+2]
            if pair in pairs:
                continue
            else:
                pairs.append(pair)
        
        # Calculate the frequencies of each pair and collecting them
        # into a list ordered in the same order of the pairs
        frequencies = [ len(re.findall(el, text)) for el in pairs ]

        # Calculate the most frequent pair, add a new rule and substitute with the new symbol
        f_max = max(frequencies)
        if f_max == 1:
            break

        new_symbol = chr(ord(new_symbol)+1)             # Using uppercase letters as new symbols
        rule = pairs[ frequencies.index(f_max) ]
        P[new_symbol] = rule
        text = re.sub(rule, new_symbol, text)

    return text, P

def CNF(text : str):
    '''
    Thif function obtain a grammar in Chomsky Normal Form obtained by RE-PAIR algorithm 
    Input:
        - text : string to compress
    Output:
        - compressed text
        - dictionary containing all the rules in CNF
    '''
    text = text.lower()
    P = {}           # Dictionary containing all the rules: set of productions
    new_symbol = chr(ord('A')-1)
    # Initial step: creating unary productions
    terminal_symbols = sorted(set(text))
    for value in terminal_symbols:
        new_symbol = chr(ord(new_symbol)+1)
        P[new_symbol] = value
    
    # Replacing all terminal symbols with non-terminal symbols just created
    for key in P.keys():
        value = P[key]
        text = re.sub( value, key, text )
    
    # Replacement step: applying the Re-Pair algorithm - replacing all occurrences of bigrams with new non-terminal symbols
    while True:
        
        # Calculate all the distinct pairs of symbols XY
        pairs = []
        for i in range(len(text)-2):
            pair = text[i:i+2]
            if pair in pairs:
                continue
            else:
                pairs.append(pair)
        
        # Calculate the frequencies of each pair and collecting them
        # into a list ordered in the same order of the pairs
        frequencies = [ len(re.findall(el, text)) for el in pairs ]

        # Calculate the most frequent pair, add a new rule and substitute with the new symbol
        f_max = max(frequencies)
        if f_max == 1:
            break

        new_symbol = chr(ord(new_symbol)+1)             # Using uppercase letters as new symbols
        rule = pairs[ frequencies.index(f_max) ]
        P[new_symbol] = rule
        text = re.sub(rule, new_symbol, text)
    
    return text, P


if __name__ == '__main__':
    print("RE-PAIR ALGORITHM AND CHOMSKY NORMAL FORM ")
    print()
    print("Insert the string you want to determine a grammar:")
    T = str(input())
    print()
    
    # Apply RE-PAIR
    print("RE-PAIR:")
    print()
    T_compressed, dictionary = re_pair(T)
    print(f"The compressed text is {T_compressed}")
    print("The grammar is composed by the following rules:")
    for key in dictionary.keys():
        print(f" {key} -> {dictionary[key]}")
    
    rules = dictionary.values()
    size = sum( len(r) for r in rules )
    print(f"The size of the grammar is {size}")

    print("-----------------------------------------------------")

    # Apply CNF using RE-PAIR
    print("CNF")
    print()
    T_compressed_1, dictionary_1 = CNF(T)
    print(f"The compressed text is {T_compressed_1}")
    print("The grammar is composed by the following rules:")
    for key in dictionary_1.keys():
        print(f" {key} -> {dictionary_1[key]}")
    
    rules_1 = dictionary_1.values()
    size_1 = sum( len(r) for r in rules_1 )
    print(f"The size of the grammar is {size_1}")