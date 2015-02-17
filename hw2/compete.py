file = open('JudgeInput (1).txt')
import re

'''
i = ''

for line in file:
    i = i + line

def isPalindrome(s):
    start = 0
    for x in range(0, len(s)):
        if s[x] == '.':
            raw = s[start:x]
            start = x + 1
            temp = raw.lower()
            if palindrome(''.join(e for e in temp if e.isalnum())):
                for x in (0,len(raw)):
                    if raw[x] == ' ':
                        raw = raw[x + 1:]
                        break
                return raw


def palindrome(s):
    result = palindromeHelper(s)
    if result == None:
        return False
    if len(result) == 1 or len(result) == 0:
        return True


def palindromeHelper(array):
    if len(array) == 0 or len(array) == 1:
        return array
    elif array[0] == array[len(array) - 1]:
        return palindromeHelper((array[1:])[:len(array) - 2])
'''

def check(s3):
    count = 0
    for x in s3:
        if x == '.':
            count = count + 1
    if count > 3:
        return 'InValid'
    li = s3.split('.')
    for x in range(0,4):
        if int(li[0]) > 255 or int(li[1]) > 255 or int(li[2]) > 255 or int(li[3]) > 255 or int(li[0]) < 0 or int(li[1]) < 0 or int(li[2]) < 0 or int(li[3]) < 0:
            return 'InValid'
        if x == 0:
            if int(li[0]) < 10 or int(li[0]) > 11:
                return 'OutRange'
        if x == 1:
            if int(li[1]) < 0 or int(li[1]) > 199:
                return 'OutRange'
        if x == 2:
            if int(li[2]) < 0 or int(li[2]) > 88:
                return 'OutRange'
        if x == 3:
            if int(li[3]) < 0 or int(li[3]) > 254:
                return 'OutRange'
    return 'InRange'

inPut = ''

for line in file:
    inPut = line.split(' ')[2]
    print(check(inPut))








