''' LAB EXERCISE:
Write a program that computes all the universal codes of integers we have studied (both encoding and decoding).

Plot for each n=1,...,1000 the lenghts of the binary, gamma, delta, Fibonacci codes.
Also consider the Rice encoding for k=5 and k=7.

Report the statistics on the following experiments:
    1. number of bits required to encode 100 integers between 1 and 100000 (consider intgers 1, 1011, 2021, ...)
    2. number of bits required to compress 100 random integers between 1 and 1000
    3. number of bits required to encode a sequence of 1000 integers with distribution chosen in advance
'''

from math import log
from matplotlib import pyplot as plt
from random import randint
from statistics import mean, median, stdev
import numpy as np
import pandas as pd



def encodingGamma(num):
    N=int(log(num,2))           #Calculate the smallest power of 2 of the number 
    B=(bin(num))[2:]            #Return a string with 0b as a prefix - take the slice without it
    gamma=N*'0'+B
    
    return gamma

def decodingGamma(gamma):
    N=0
    i=0
    while gamma[i] == 0:
        N+=1
        i+=1
    g=gamma[N:]
    num=int(g,2)
    
    return num

def encodingDelta(num):
    N=int(log(num,2))           #Calculate the smallest power of 2 of the number 
    a=encodingGamma(N+1)
    B=(bin(num))[3:]            #Remove the prefix 0b and the most significant bit of the binary representation of the number N+1
    delta=a+B
    
    return delta

def decodingDelta(delta):
    i=0
    L=0
    while delta[i] == '0':
        L+=1
        i+=1
    d=delta[L : 2*L+1]          #Consider L+1 bits from the first 1 included
    N=int(d,2)-1                #Calculate the number N
    b=delta[2*L+1 :]            #Consider the remaining N bits of delta
    a= '1' + b
    num=int(a, 2)               #Calculate the integer number of the binary representation of b prepended by 1
    
    return num

def fibonacciNum(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacciNum(n-1) + fibonacciNum(n-2)

#Function needed on Fibonacci code to determine the largest Fibonacci number equal or less than the integer we wanto to encode
def nearestSmallerFib(n):
    f0=0
    f1=1
    f2=1
    
    i=2
    while f2<=n:
        f0=f1
        f1=f2
        f2=f0+f1
        i+=1
    return f1, i-1

def encodingFibonacci(n):
    pos=[]                      #List used to track the i-th fibonacci number that satisfies the Zeckendorf Theorem
                                #list contains only the value i
    while n != 0:
        x=nearestSmallerFib(n)
        r=n-x[0]
        pos.append(x[1]-2)
        n=r
    
    pos.reverse()               #Increasing order of positions - need them to insert 1s on the codeword
    fib=''
    m=max(pos)                  #Maximum position to put '1' and represents the len of the codeword
    for j in range(m+1):
        if j in pos:
            fib += '1'
        else:
            fib += '0'  
    
    fib = fib + '1'             #Adding the extra 1 to obtain a prefix code
    
    return fib

def decodingFibonacci(fib):
    fib = fib[: len(fib)-1]     #Remove the final 1
    
    val = []                    #Create a list of tuples in which there is a couple (bit, numFib)
                                #In this way, it will sum the fibonacci number corresponding to only bit 1
    for i in range(len(fib)):
        F=fibonacciNum(i+2)
        val.append(( fib[i] , F ))
    num = 0
    for j in range(len(val)):
        if val[j][0] == '1':
            num = num + val[j][1]
    
    return num 
  
def encodingLevenshtein(n):
    lev=''
    if n == 0:              #The code of zero is 0
        lev += '0'
        return lev 
    
    C = 1                   #Initialize the step count to 1
    while True:
        B=(bin(n))[2:]      #Remove the prefix 0b to the binary representation
        b=B[1:]             #Remove the leading 1 to the beginning of the code
        
        lev = b + lev       #Saving the binary representation for the result
        M = len(b)          #Variable of the number of bits remaining from the binary representation without the leading 1
        if M != 0:
            C += 1
            n = M
        else:
            break
    
    lev = C * '1' + '0' + lev 
    return lev 

def decodingLevenshtein(lev):
    #Counting the number of 1s at the beginning of the code until the first 0
    count = 0
    for i in range(len(lev)):
        if lev[i] == '1':
            count += 1
        else: 
            break
    
    if count == 0:              #Remember: the code of zero is 0
        return 0
    else:
        N = 1                   #Variable to count the bits to read
        lev = lev[count+1 :]    #Start to scan the code after the first 0
        for i in range(1,count): 
            b = lev[:N]         #Reads N bits
            lev = lev[N:]       #Continue the scanning of the code after the N bits of the previous step
            B = '1' + b         #Prepend '1'
            num = int(B,2)      
            N = num             #Assign the resulting value to N
            
        return N
     
def encodingRice(n,k):
    #Calcutation of the quotient
    Q = int( (n-1)/(2**k) )
    q = ''
    for i in range(Q):          #Unary representation in Q+1 bits
        q += '0'
    q += '1'
    
    #Calculation of the remainder
    R = n - (2**k) * Q - 1
    r = (bin(R))[2:]            #Binary representation without the prefix 0b
    if len(r) != k:             #Use k bits
        z = k - len(r)
        for i in range(z):
            r = '0' + r
    
    rice = q + r
    return rice 

def decodingRice(rice):
    #Calculation of q
    count = 0
    for i in range(len(rice)):
        if rice[i] == '0':
            count += 1
        else:
            break
    q = count 
    
    k = len( rice[count+1:] )   #Skip the delimiting 1 and consider the rest of the code
    r = int(rice[count+1:], 2) 
    
    n = q * (2**k) + r + 1
    return n

#REPORT: functions to use in the main where it will plot the statistics
#Defining a function for the experiment1
def experiment1():
    num_1 = []                  #Generate the 100 integers between 1 and 100000
    n = 1
    while n <= 100000:
        num_1.append(n)
        n += 1010               #Considering numbers such as 1, 1011, 2021, 3031,...

    #List of codeword for each code: Gamma, Delta, Fibonacci, Levenshtein 
    code_g = [] 
    code_d = []
    code_f = []
    code_l = [] 
    for i in range(len(num_1)):
        g = encodingGamma(num_1[i])
        code_g.append(g)
        d = encodingDelta(num_1[i])
        code_d.append(d)
        f = encodingFibonacci(num_1[i])
        code_f.append(f)
        l = encodingLevenshtein(num_1[i])
        code_l.append(l)
    
    #List of bits used for each code
    bit_g = []
    bit_d = []
    bit_f = []
    bit_l = []
    for i in range(len(code_g)):
        b = len(code_g[i])
        bit_g.append(b)
    for i in range(len(code_d)):
        b1 = len(code_d[i])
        bit_d.append(b1)
    for i in range(len(code_f)):
        b2 = len(code_f[i])
        bit_f.append(b2)
    for i in range(len(code_l)):
        b3 = len(code_l[i])
        bit_l.append(b3)
    
    return num_1, bit_g, bit_d, bit_f, bit_l 

#Defining a function for the experiment2
def experiment2():
    num_2 = []                  #Generate the 100 random integers between 1 and 1000 
    while len(num_2) != 100: 
        n = randint(1, 1001)
        if n not in num_2:
            num_2.append(n)
        else:
            continue
    num_2 = sorted(num_2)       #Increasing order of numbers              

    #List of codeword for each code: Gamma, Delta, Fibonacci, Levenshtein 
    code_g = [] 
    code_d = []
    code_f = []
    code_l = [] 
    for i in range(len(num_2)):
        g = encodingGamma(num_2[i])
        code_g.append(g)
        d = encodingDelta(num_2[i])
        code_d.append(d)
        f = encodingFibonacci(num_2[i])
        code_f.append(f)
        l = encodingLevenshtein(num_2[i])
        code_l.append(l)
    
    #List of bits used for each code
    bit_g = []
    bit_d = []
    bit_f = []
    bit_l = []
    for i in range(len(code_g)):
        b = len(code_g[i])
        bit_g.append(b)
    for i in range(len(code_d)):
        b1 = len(code_d[i])
        bit_d.append(b1)
    for i in range(len(code_f)):
        b2 = len(code_f[i])
        bit_f.append(b2)
    for i in range(len(code_l)):
        b3 = len(code_l[i])
        bit_l.append(b3)
    
    return num_2, bit_g, bit_d, bit_f, bit_l 

#Defining a function for the experiment3
#Generate the 1000 integers with a distribution chosen in advance: chosing a distribution of odd numbers
def experiment3():
    num_3 = []                  #List of 1000 odd integers                 
    while len(num_3) != 1000: 
        for n in range(1, 2001):
            if n%2 != 0:
                num_3.append(n)
            else:
                continue                   

    #List of codeword for each code: Gamma, Delta, Fibonacci, Levenshtein 
    code_g_odd = [] 
    code_d_odd = []
    code_f_odd = []
    code_l_odd = [] 
    for i in range(len(num_3)):
        g = encodingGamma(num_3[i])
        code_g_odd.append(g)
        d = encodingDelta(num_3[i])
        code_d_odd.append(d)
        f = encodingFibonacci(num_3[i])
        code_f_odd.append(f)
        l = encodingLevenshtein(num_3[i])
        code_l_odd.append(l)
    
    #List of bits used for each code
    bit_g_odd = []
    bit_d_odd = []
    bit_f_odd = []
    bit_l_odd = []
    for i in range(len(code_g_odd)):
        b = len(code_g_odd[i])
        bit_g_odd.append(b)
    for i in range(len(code_d_odd)):
        b1 = len(code_d_odd[i])
        bit_d_odd.append(b1)
    for i in range(len(code_f_odd)):
        b2 = len(code_f_odd[i])
        bit_f_odd.append(b2)
    for i in range(len(code_l_odd)):
        b3 = len(code_l_odd[i])
        bit_l_odd.append(b3)
        
    return num_3, bit_g_odd, bit_d_odd, bit_f_odd, bit_l_odd

#Defining a function for the experiment1,2,3 about Rice codes - studying the bits based on different values of the parameter k, chosing from 1 to 10
def experiment1_2_3_Rice():
    num_1 = experiment1()
    num_2 = experiment2()
    num_3 = experiment3()

    length_1 = []
    for k in range(1, 11):
        L = (k, [])
        for n in num_1[0]:
            cw = encodingRice(n,k)
            l = len(cw)
            L[1].append(l)
        length_1.append(L)
    
    length_2 = []
    for k in range(1, 11):
        L = (k, [])
        for n in num_2[0]:
            cw = encodingRice(n,k)
            l = len(cw)
            L[1].append(l)
        length_2.append(L)
    
    length_3 = []
    for k in range(1, 11):
        L = (k, [])
        for n in num_3[0]:
            cw = encodingRice(n,k)
            l = len(cw)
            L[1].append(l)
        length_3.append(L)
    
    return length_1, length_2, length_3, num_1[0], num_2[0], num_3[0]


if __name__ == '__main__':
    print("INTEGER ENCODING")
    print()
    print("What do you want to do?")
    print("a. Encoding an integer number")
    print("b. Plotting of experiments on integer coding")
    answer = str(input())
    while ( answer != 'a' and answer != 'b' ):
        answer = str(input("Please, try again ... "))
    
    if answer == 'a':

        x = int(input("Insert the number you want to encode "))
        while x < 0:
            x = int(input("Please, insert another positive integer: "))
        
        #Calculation of each code for the integer entered
        gamma_x = encodingGamma(x)
        g_x = decodingGamma(gamma_x)
        delta_x = encodingDelta(x)
        d_x = decodingDelta(delta_x)
        fib_x = encodingFibonacci(x)
        f_x = decodingFibonacci(fib_x)
        lev_x = encodingFibonacci(x)
        l_x = decodingFibonacci(lev_x)
        k = int(input("Insert a parameter for Rice code: "))
        while k < 0:
            k = int(input("Please, insert a positive integer: "))
        rice_x = encodingRice(x, k)
        r_x = decodingRice(rice_x)

        print("ENCODINGS OF ", x)
        print("Gamma code: ", gamma_x,"---", "Decode: ", g_x)
        print("Delta code: ", delta_x,"---", "Decode: ", d_x)
        print("Fibonacci code: ", fib_x,"---", "Decode: ", f_x)
        print("Levenshtein code: ", lev_x,"---", "Decode: ", l_x)
        print("Rice code: ", rice_x,"---", "Decode: ", r_x)
    
    else:
        
        #Plot of the lengths of code: binary, Gamma, Delta, Fibonacci, Rice with k=5 and k=7, for numbers n=1,...,1000
        bin_lengths = []
        for n in range(1, 1001):
            b = (bin(n))[2:]              #Remove the prefix 0b
            l = len(b)
            bin_lengths.append(l)
        y1 = bin_lengths

        gamma_lengths = []
        for n in range(1, 1001):
            g = encodingGamma(n)
            l1 = len(g)
            gamma_lengths.append(l1)
        y2 = gamma_lengths

        delta_lengths = []
        for n in range(1, 1001):
            d = encodingDelta(n)
            l2 = len(d)
            delta_lengths.append(l2)
        y3 = delta_lengths 

        fib_lengths = []
        for n in range(1, 1001):
            f = encodingFibonacci(n)
            l3 = len(f)
            fib_lengths.append(l3)
        y4 = fib_lengths

        rice5_lengths = []
        for n in range(1, 1001):
            r = encodingRice(n,5)
            l4 = len(r)
            rice5_lengths.append(l4)
        y5 = rice5_lengths

        rice7_lengths = []
        for n in range(1, 1001):
            r1 = encodingRice(n,7)
            l5 = len(r1)
            rice7_lengths.append(l5)
        y6 = rice7_lengths

        x = []
        for n in range(1, 1001):
            x.append(n)

        plt.style.use("seaborn-v0_8-whitegrid") 
        plt.plot(x, y1, label="Binary code", color="green")
        plt.plot(x, y2, label="Gamma code", color="red")
        plt.plot(x, y3, label="Delta code", color="yellow")
        plt.plot(x, y4, label="Fibonacci code", color="black")
        plt.plot(x, y5, label="Rice code, k=5", color="purple")
        plt.plot(x, y6, label="Rice code, k=7", color="orange")
        plt.legend()
        plt.title("Lengths of codeword of integers from 1 to 1000")
        plt.xlabel("Integer n")
        plt.ylabel("Lengths")
        plt.show()

        #EXPERIMENT 1: PLOTS AND STATISTICS
        fig1, ((ax1g, ax1d), (ax1f, ax1l)) = plt.subplots(nrows=2, ncols=2, sharex=True, label="Experiment1_Plot")
        num1, y1g, y2d, y3f, y4l = experiment1()

        ax1g.plot(num1, y1g, label="Gamma code", color="red")
        ax1g.set_title("Gamma code", fontsize=10)
        ax1g.set_xlabel("Numbers", fontsize=7.5)
        ax1g.set_ylabel("Bits", fontsize=7.5)

        ax1d.plot(num1, y2d, label="Delta code", color="green")
        ax1d.set_title("Delta code", fontsize=10)
        ax1d.set_xlabel("Numbers", fontsize=7.5)
        ax1d.set_ylabel("Bits", fontsize=7.5)

        ax1f.plot(num1, y3f, label="Fibonacci code", color="purple")
        ax1f.set_title("Fibonacci code", fontsize=10)
        ax1f.set_xlabel("Numbers", fontsize=7.5)
        ax1f.set_ylabel("Bits", fontsize=7.5)

        ax1l.plot(num1, y4l, label="Levenshtein code", color="orange")
        ax1l.set_title("Levenshtein code", fontsize=10)
        ax1l.set_xlabel("Numbers", fontsize=7.5)
        ax1l.set_ylabel("Bits", fontsize=7.5)

        plt.style.use("seaborn-v0_8-whitegrid")
        
        #Gamma code statistics
        min1_g = min(y1g)
        max1_g = max(y1g)
        fig1a, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, label="Experiment1_Gamma code")
        ax1.hist(y1g, color="red")                                  #Asymmetric distribution
        ax2.boxplot(y1g)
        median1_g = median(y1g)
        p1g, p2g = np.percentile(y1g, [25, 75])
        iqr1_g = p2g - p1g                                          #Range interquartile, IQR, defined as the difference between the third and first quartile

        #Delta code statistics 
        min1_d = min(y2d)
        max1_d = max(y2d)
        fig1b, (ax11, ax22) = plt.subplots(nrows=1, ncols=2, label="Experiment1_Delta code")
        ax11.hist(y2d, color="green")                             #Asymmetric distribution
        ax22.boxplot(y2d)
        median1_d = median(y2d)
        p1d, p2d = np.percentile(y2d, [25, 75])                   #Range interquartile, IQR, defined as the difference between the third and first quartile
        iqr1_d = p2d - p1d

        #Fibonacci code statistics
        min1_f = min(y3f)
        max1_f = max(y3f)
        fig1c, (ax_1, ax_2) = plt.subplots(nrows=1, ncols=2, label="Experiment1_Fibonacci code")
        ax_1.hist(y3f, color="purple")                              #Asymmetric distribution
        ax_2.boxplot(y3f)
        median1_f = median(y3f)
        p1f, p2f = np.percentile(y3f, [25, 75])                     #Range interquartile, IQR, defined as the difference between the third and first quartile
        iqr1_f = p2f - p1f

        #Levenshtein code statistics
        min1_l = min(y4l)
        max1_l = max(y4l)
        fig1d, (ax_11, ax_22) = plt.subplots(nrows=1, ncols=2, label="Experiment1_Levenshtein code")
        ax_11.hist(y4l, color="orange")                             #Asymmetric distribution
        ax_22.boxplot(y4l)
        median1_l = median(y4l)
        p1l, p2l = np.percentile(y4l, [25, 75])                     #Range interquartile, IQR, defined as the difference between the third and first quartile
        iqr1_l = p2l - p1l 


        #Table of statistics
        dict1 = {
            'Minimum' : [min1_g, min1_d, min1_f, min1_l],
            'Maximum' : [max1_g, max1_d, max1_f, max1_l],
            'Median' : [median1_g, median1_d, median1_f, median1_l],
            'IQR' : [iqr1_g, iqr1_d, iqr1_f, iqr1_l]
        }
        df1 = pd.DataFrame(dict1, index=["Gamma code", "Delta code", "Fibonacci code", "Levenshtein code"])
        print("Statistics Experiment1:")
        print()
        print(df1)

        plt.show()


        #EXPERIMENT 2: PLOTS AND STATISTICS
        fig2, ((ax2g, ax2d), (ax2f, ax2l)) = plt.subplots(nrows=2, ncols=2, sharex=True, label="Experiment2_Plot")
        num2, z1g, z2d, z3f, z4l = experiment2()

        ax2g.plot(num2, z1g, label="Gamma code", color="red")
        ax2g.set_title("Gamma code", fontsize=10)
        ax2g.set_xlabel("Numbers", fontsize=7.5)
        ax2g.set_ylabel("Bits", fontsize=7.5)

        ax2d.plot(num2, z2d, label="Delta code", color="green")
        ax2d.set_title("Delta code", fontsize=10)
        ax2d.set_xlabel("Numbers", fontsize=7.5)
        ax2d.set_ylabel("Bits", fontsize=7.5)

        ax2f.plot(num2, z3f, label="Fibonacci code", color="purple")
        ax2f.set_title("Fibonacci code", fontsize=10)
        ax2f.set_xlabel("Numbers", fontsize=7.5)
        ax2f.set_ylabel("Bits", fontsize=7.5)

        ax2l.plot(num2, z4l, label="Levenshtein code", color="orange")
        ax2l.set_title("Levenshtein code", fontsize=10)
        ax2l.set_xlabel("Numbers", fontsize=7.5)
        ax2l.set_ylabel("Bits", fontsize=7.5)

        plt.style.use("seaborn-v0_8-whitegrid")

        #Gamma code statistics
        min2_g = min(z1g)
        max2_g = max(z1g)
        fig2a, (ax01, ax02) = plt.subplots(nrows=1, ncols=2, label="Experiment2_Gamma code")
        ax01.hist(z1g, color="red")                                 #Asymmetric distribution
        ax02.boxplot(z1g)
        median2_g = median(z1g)
        p1_g, p2_g = np.percentile(z1g, [25, 75])                   #Range interquartile, IQR, defined as the difference between the third and first quartile
        iqr2_g = p2_g - p1_g

        #Delta code statistics 
        min2_d = min(z2d)
        max2_d = max(z2d)
        fig2b, (ax01_1, ax02_2) = plt.subplots(nrows=1, ncols=2, label="Experiment2_Delta code")
        ax01_1.hist(z2d, color="green")                             #Asymmetric distribution
        ax02_2.boxplot(z2d)
        median2_d = median(z2d)
        p1_d, p2_d = np.percentile(z2d, [25, 75])                   #Range interquartile, IQR, defined as the difference between the third and first quartile
        iqr2_d = p2_d - p1_d

        #Fibonacci code statistics
        min2_f = min(z3f)
        max2_f = max(z3f)
        fig2c, (ax_01, ax_02) = plt.subplots(nrows=1, ncols=2, label="Experiment2_Fibonacci code")
        ax_01.hist(z3f, color="purple")                              #Asymmetric distribution
        ax_02.boxplot(z3f)
        median2_f = median(z3f)
        p1_f, p2_f = np.percentile(z3f, [25, 75])                     #Range interquartile, IQR, defined as the difference between the third and first quartile
        iqr2_f = p2_f - p1_f

        #Levenshtein code statistics
        min2_l = min(z4l)
        max2_l = max(z4l)
        fig2d, (ax1_01, ax2_02) = plt.subplots(nrows=1, ncols=2, label="Experiment2_Levenshtein code")
        ax1_01.hist(z4l, color="orange")                             #Asymmetric distribution
        ax2_02.boxplot(z4l)
        median2_l = median(z4l)
        p1_l, p2_l = np.percentile(z4l, [25, 75])                     #Range interquartile, IQR, defined as the difference between the third and first quartile
        iqr2_l = p2_l - p1_l 
        

        #Table of statistics
        dict2 = {
            'Minimum' : [min2_g, min2_d, min2_f, min2_l],
            'Maximum' : [max2_g, max2_d, max2_f, max2_l],
            'Median' : [median2_g, median2_d, median2_f, median2_l],
            'IQR' : [iqr2_g, iqr2_d, iqr2_f, iqr2_l]
        }
        df2 = pd.DataFrame(dict2, index=["Gamma code", "Delta code", "Fibonacci code", "Levenshtein code"])
        print("Statistics Experiment2:")
        print()
        print(df2)

        plt.style.use("seaborn-v0_8-whitegrid")
        plt.show()
        
        #EXPERIMENT 3: PLOTS AND STATISTICS
        fig3_odd, ((ax3g, ax3d), (ax3f, ax3l)) = plt.subplots(nrows=2, ncols=2, sharex=True, label="Experiment3_Plot")
        num3, t1g, t2d, t3f, t4l = experiment3()

        ax3g.plot(num3, t1g, label="Gamma code", color="red")
        ax3g.set_title("Gamma code", fontsize=10)
        ax3g.set_xlabel("Numbers", fontsize=7.5)
        ax3g.set_ylabel("Bits", fontsize=7.5)

        ax3d.plot(num3, t2d, label="Delta code", color="green")
        ax3d.set_title("Delta code", fontsize=10)
        ax3d.set_xlabel("Numbers", fontsize=7.5)
        ax3d.set_ylabel("Bits", fontsize=7.5)

        ax3f.plot(num3, t3f, label="Fibonacci code", color="purple")
        ax3f.set_title("Fibonacci code", fontsize=10)
        ax3f.set_xlabel("Numbers", fontsize=7.5)
        ax3f.set_ylabel("Bits", fontsize=7.5)

        ax3l.plot(num3, t4l, label="Levenshtein code", color="orange")
        ax3l.set_title("Levenshtein code", fontsize=10)
        ax3l.set_xlabel("Numbers", fontsize=7.5)
        ax3l.set_ylabel("Bits", fontsize=7.5)

        plt.style.use("seaborn-v0_8-whitegrid")

        #Gamma code statistics
        min3_g = min(t1g)
        max3_g = max(t1g)
        fig3a, (ax31, ax32) = plt.subplots(nrows=1, ncols=2, label="Experiment3_Gamma code")
        ax31.hist(t1g, color="red")                                     #Asymmetric distribution
        ax32.boxplot(t1g)
        median3_g = median(t1g)
        p1__g, p2__g = np.percentile(t1g, [25, 75])                     #Range interquartile, IQR, defined as the difference between the third and first quartile
        iqr3_g = p2__g - p1__g

        #Delta code statistics 
        min3_d = min(t2d)
        max3_d = max(t2d)
        fig3b, (ax31_1, ax31_2) = plt.subplots(nrows=1, ncols=2, label="Experiment3_Delta code")
        ax31_1.hist(t2d, color="green")                                 #Asymmetric distribution
        ax31_2.boxplot(t2d)
        median3_d = median(t2d)
        p1__d, p2__d = np.percentile(t2d, [25, 75])                     #Range interquartile, IQR, defined as the difference between the third and first quartile
        iqr3_d = p2__d - p1__d

        #Fibonacci code statistics
        min3_f = min(t3f)
        max3_f = max(t3f)
        fig3c, (ax3_01, ax3_02) = plt.subplots(nrows=1, ncols=2, label="Experiment3_Fibonacci code")
        ax3_01.hist(t3f, color="purple")                                #Asymmetric distribution
        ax3_02.boxplot(t3f)
        median3_f = median(t3f)
        p1__f, p2__f = np.percentile(t3f, [25, 75])                     #Range interquartile, IQR, defined as the difference between the third and first quartile
        iqr3_f = p2__f - p1__f

        #Levenshtein code statistics
        min3_l = min(t4l)
        max3_l = max(t4l)
        fig3d, (ax3_1, ax3_2) = plt.subplots(nrows=1, ncols=2, label="Experiment3_Levenshtein code")
        ax3_1.hist(t4l, color="orange")                                 #Asymmetric distribution
        ax3_2.boxplot(t4l)
        median3_l = median(t4l)
        p1__l, p2__l = np.percentile(t4l, [25, 75])                     #Range interquartile, IQR, defined as the difference between the third and first quartile
        iqr3_l = p2__l - p1__l


        #Table of statistics
        dict3 = {
            'Minimum' : [min3_g, min3_d, min3_f, min3_l],
            'Maximum' : [max3_g, max3_d, max3_f, max3_l],
            'Median' : [median3_g, median3_d, median3_f, median3_l],
            'IQR' : [iqr3_g, iqr3_d, iqr3_f, iqr3_l]
        }
        df3 = pd.DataFrame(dict3, index=["Gamma code", "Delta code", "Fibonacci code", "Levenshtein code"])
        print("Statistics Experiment3:")
        print()
        print(df3)
        
        plt.style.use("seaborn-v0_8-whitegrid")
        plt.show()

        #Experiment 1, 2, 3 of Rice codes
        fig4, (ax4_1, ax4_2, ax4_3) = plt.subplots(nrows=3, ncols=1, label="Experiments1,2,3_Rice codes")
        l1, l2, l3, n1, n2, n3 = experiment1_2_3_Rice()

        #1:
        l1_1 = l1[0][1]
        l1_2 = l1[1][1]
        l1_3 = l1[2][1]
        l1_4 = l1[3][1]
        l1_5 = l1[4][1]
        l1_6 = l1[5][1]
        l1_7 = l1[6][1]
        l1_8 = l1[7][1]
        l1_9 = l1[8][1]
        l1_10 = l1[9][1]
        
        ax4_1.plot(n1,l1_1, label="k=1")
        ax4_1.plot(n1,l1_2, label="k=2")
        ax4_1.plot(n1,l1_3, label="k=3")
        ax4_1.plot(n1,l1_4, label="k=4")
        ax4_1.plot(n1,l1_5, label="k=5")
        ax4_1.plot(n1,l1_6, label="k=6")
        ax4_1.plot(n1,l1_7, label="k=7")
        ax4_1.plot(n1,l1_8, label="k=8")
        ax4_1.plot(n1,l1_9, label="k=9")
        ax4_1.plot(n1,l1_10, label="k=10")
        ax4_1.set_title("Experiment 1", fontsize=10)
        ax4_1.set_ylabel("Bits", fontsize=7.5)

        #2:
        l2_1 = l2[0][1]
        l2_2 = l2[1][1]
        l2_3 = l2[2][1]
        l2_4 = l2[3][1]
        l2_5 = l2[4][1]
        l2_6 = l2[5][1]
        l2_7 = l2[6][1]
        l2_8 = l2[7][1]
        l2_9 = l2[8][1]
        l2_10 = l2[9][1]
        
        ax4_2.plot(n2,l2_1, label="k=1")
        ax4_2.plot(n2,l2_2, label="k=2")
        ax4_2.plot(n2,l2_3, label="k=3")
        ax4_2.plot(n2,l2_4, label="k=4")
        ax4_2.plot(n2,l2_5, label="k=5")
        ax4_2.plot(n2,l2_6, label="k=6")
        ax4_2.plot(n2,l2_7, label="k=7")
        ax4_2.plot(n2,l2_8, label="k=8")
        ax4_2.plot(n2,l2_9, label="k=9")
        ax4_2.plot(n2,l2_10, label="k=10")
        ax4_2.set_title("Experiment 2", fontsize=10)
        ax4_2.set_ylabel("Bits", fontsize=7.5)

        #3:
        l3_1 = l3[0][1]
        l3_2 = l3[1][1]
        l3_3 = l3[2][1]
        l3_4 = l3[3][1]
        l3_5 = l3[4][1]
        l3_6 = l3[5][1]
        l3_7 = l3[6][1]
        l3_8 = l3[7][1]
        l3_9 = l3[8][1]
        l3_10 = l3[9][1]
        
        ax4_3.plot(n3,l3_1, label="k=1")
        ax4_3.plot(n3,l3_2, label="k=2")
        ax4_3.plot(n3,l3_3, label="k=3")
        ax4_3.plot(n3,l3_4, label="k=4")
        ax4_3.plot(n3,l3_5, label="k=5")
        ax4_3.plot(n3,l3_6, label="k=6")
        ax4_3.plot(n3,l3_7, label="k=7")
        ax4_3.plot(n3,l3_8, label="k=8")
        ax4_3.plot(n3,l3_9, label="k=9")
        ax4_3.plot(n3,l3_10, label="k=10")
        ax4_3.set_title("Experiment 3", fontsize=10)
        ax4_3.set_xlabel("Numbers", fontsize=7.5)
        ax4_3.set_ylabel("Bits", fontsize=7.5)
        
        fig4.legend()
        fig4.suptitle("Rice codes")
        plt.style.use("seaborn-v0_8-whitegrid")
        

        #Rice codes statistics
        #1:
        L1 = l1_1 + l1_2 + l1_3 + l1_4 + l1_5 + l1_6 + l1_7 + l1_8 + l1_9 + l1_10
        min1_r = min(L1)
        max1_r = max(L1)
        fig4a, (ax41, ax42) = plt.subplots(nrows=1, ncols=2, label="Experiment1_Rice codes")
        ax41.hist(L1, color="green")
        ax42.boxplot(L1)
        median1_r = median(L1)
        p1_r, p2_r = np.percentile(L1, [25,75])
        iqr1_r = p2_r - p1_r 
        fig4a.suptitle("Experiment 1 - Rice codes - k=1,..., 10")

        #2:
        L2 = l2_1 + l2_2 + l2_3 + l2_4 + l2_5 + l2_6 + l2_7 + l2_8 + l2_9 + l2_10
        min2_r = min(L2)
        max2_r = max(L2)
        fig4b, (ax41a, ax42a) = plt.subplots(nrows=1, ncols=2, label="Experiment2_Rice codes")
        ax41a.hist(L2, color="blue")
        ax42a.boxplot(L2)
        median2_r = median(L2)
        p1__r, p2__r = np.percentile(L2, [25,75])
        iqr2_r = p2__r - p1__r 
        fig4b.suptitle("Experiment 2 - Rice codes - k=1,..., 10")

        #3:
        L3 = l3_1 + l3_2 + l3_3 + l3_4 + l3_5 + l3_6 + l3_7 + l3_8 + l3_9 + l3_10
        min3_r = min(L3)
        max3_r = max(L3)
        fig4c, (ax41c, ax42c) = plt.subplots(nrows=1, ncols=2, label="Experiment3_Rice codes")
        ax41c.hist(L3, color="purple")
        ax42c.boxplot(L3)
        median3_r = median(L3)
        p1___r, p2___r = np.percentile(L3, [25,75])
        iqr3_r = p2___r - p1___r 
        fig4c.suptitle("Experiment 3 - Rice codes - k=1,..., 10")

        #Table of statistics
        dict3 = {
            'Minimum' : [min1_r, min2_r, min3_r],
            'Maximum' : [max1_r, max2_r, max3_r],
            'Median' : [median1_r, median2_r, median3_r],
            'IQR' : [iqr1_r, iqr2_r, iqr3_r]
        }
        df4 = pd.DataFrame(dict3, index=["Experiment 1", "Experiment 2", "Experiment 3"])
        print("Statistics Rice codes:")
        print()
        print(df4)

        plt.style.use("seaborn-v0_8-whitegrid")
        plt.show()
