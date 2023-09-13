''' EXERCISE 1: 
    Write a program that applies the Sardinas-Patterson algorithm and returns the type of code received as input.
    
    - Apply the algorithm to test whether C={012, 0123, 4, 310, 1024, 2402, 2401, 4013} is UD.
    - Apply the algorithm to verify which of the codes:
        C_1={10, 010, 1, 1110}
        C_2={0, 001, 101, 11}
        C_3={0, 2, 03, 011, 104, 341, 11234}
        C_4={01, 10, 001, 100, 000, 111}
      
        are UD.'''



#Define a function that compares 2 codewords and determines if the first one is a prefix of the second one
#If so, it returns the suffix

def prefix(s1,s2):
    a=len(s1)
    b=len(s2)
    
    if a == b or a > b:
        return False
    elif a < b:
        i=0
        while i < a and s1[i] == s2[i]:
            i+=1
        if i == a:
            s=s2[i:]
            return s
        else:
            return False

def Sardinas_Patterson(C):
    #Use a list of 2-tuples to store the sets
    #A 2-tuple is composed as (i, S_i), where S_i is the set of suffixes
    
    S=[(0, C)]                                          #List that contains all the sets S_i, starting with S_0=C
    
    while True:
        
        i=len(S)-1
        newSet=set()
        
        for cw in C:                                    #Creation of set S_i                  
            for el in S[i][1]:
                s1=prefix(cw,el)
                s2=prefix(el,cw)
                
                if s1 != False:
                    newSet.add(s1)
                elif s2 != False:
                    newSet.add(s2)
                else:
                    continue 
        S.insert(i+1, (i+1, newSet))                     
       
        if C & S[i+1][1] != set() :                     #Halting conditions
            print("The code", C, "is NOT UD.")
            break 
        elif S[i+1][1] == set() :
            print("The code", C, "is UD.")
            break 
        else:
            j=0
            while j < i+1:
                if S[i+1][1].issubset(S[j][1]) and S[i+1][1].issuperset(S[j][1]):
                    print("The code", C, "is UD.")                  
                    break
                else:
                    j+=1
            if j < i+1:
                break
        continue
   
    print()
    print("The sets created are the following:")
    for k in range(len(S)):
        print(k, "=", S[k][1])



if __name__ == '__main__':
    print("SARDINAS-PATTERSON ALGORITHM")
    print()
    print("Insert the codewords of the code C you want to verify:")
    C=set() #Variable that contains the code C that the user insert
    while True:
        c=str(input())
        if c == '':
            break
        else:
            C.add(c)
    print("The code is")
    print("C=", C)
    print("____________________________________________________________")
    print()
    Sardinas_Patterson(C)
