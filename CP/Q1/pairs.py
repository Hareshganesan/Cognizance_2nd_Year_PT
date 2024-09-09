import math
import os
import random
import re
import sys


def pairs(k, arr):
    arr_set = set(arr)
    count = 0
    
    for x in arr:
        if x + k in arr_set:
            count += 1
    
    return count

    
#This is for testing the given test cases in the hackerrank.
if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    k = int(first_multiple_input[1])

    arr = list(map(int, input().rstrip().split()))

    result = pairs(k, arr)

    fptr.write(str(result) + '\n')

    fptr.close()
