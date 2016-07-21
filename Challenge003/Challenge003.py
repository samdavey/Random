
# coding: utf-8

# ## Problem Statement
# https://github.com/C3/weekly-challenge/tree/master/003-cototbp
# 
# ### COTOTBP
# 
# A while back you flashed a firmware-level key-logger into a Nokia 3210. You forgot about it, then gave the phone away.
# 
# Years later you discover a message in /root/.mail on a host you own. Write a script to decrypt the contents and find out what happened.
# ```
# 0-9: keypad presses
#   c: clear (backspace) button press
#   p: pause (over 1 second elapsed)
#   _: long pause (over 10 minutes elapsed)
# ```
# As I remember, the map was roughly:
# ```
# space: 0
# 0: 00
# backspace: c
# a: 2
# b: 22
# c: 222
# 2: 2222
# d: 3
# e: 33
# f: 333
# 3: 3333
# g: 4
# h: 44
# i: 444
# 4: 4444
# j: 5
# k: 55
# l: 555
# 5: 5555
# m: 6
# n: 66
# o: 666
# 6: 6666
# p: 7
# q: 77
# r: 777
# s: 7777
# 7: 77777
# t: 8
# u: 88
# v: 888
# 8: 8888
# w: 9
# x: 99
# y: 999
# z: 9999
# 9: 99999
# .: 1
# ,: 11
# ?: 111
# !: 1111
# 1: 11111
# ```
# The message
# ```
# From: "Ph0n3" <Ph0n3@whitehat.net.nz>
# To: "root" <root@localhost>
# Date: Wed, 5 June 2002 12:01:50 +1200
# Subject: Buttuns
# 
# 44339990844p444777706444066906688622p2111108998093366088022p2550333602224448999_66202277700p0480444803337776020688881_6664440844330727777p7777930444777702p2224443p3332p222330777733p33099907776668866308888_444777705337777p7777cccc53366p669990222666p64446641110555338063305566p666077774433777707p777338p899906644422233cccc446668ccc222666p666555_9244480444555p555022330844337773307777666p666p660366644466011111666600p0666p660611111022244332225544481111_66204440442888086660443323022p2p222550866608443307777828444666p660444660206p666p66844_p44339990333882225509996668809337773309996668808443377733111066p66610366604440222p27773302p2266688p809996668877704488777722p2663111066p666_77778870626602233p3366020555666p66403299909443377733088028111_777744337777055566677778022777666066p66603p3325551_777444p4p4480777733p330880777766_8666p666p666p666068822244_9996661102228870666333083320666p66084433022p2p22255076667772224402233084433777331111p1111_222p26604440442888088777077774447777833777p77770668862233777111_4433999022p2p22330444605553328884446608666966044466020333p3390329997777cccccccccccccccccccccccccccccccc444605553328884446603666cc8666p66444p4p448104448092777703338866cccccccccc7777666777p777999ccccc55566688833099966688cccc1
# .
# ```
# So, what does COTOTBP stand for and What's the password? Something like this came up in a hacking CTF lately, hope you enjoy.
# 
# ## Solution Design
# 
# 1. Decode from multitap, in order of longest multitap sequence to shortest, and offset the resulting character to ensure that it cannot be accidentally re-decoded
# 2. Strip out all pauses: they have done their job once the multitap-decode is complete
# 3. Apply the backspaces using regex-replace: repeatedly replace all instances of 'any chaacter but c that is followed by c'. 
# 4. Decode the offset characters to their original character set. This is done after applying the backspace (represented by c) to avoid actual 'c's in the text being treated as backspaces.

# In[31]:

# imports: regex
import re

code_string = '44339990844p444777706444066906688622p2111108998093366088022p2550333602224448999_66202277700p0480444803337776020688881_6664440844330727777p7777930444777702p2224443p3332p222330777733p33099907776668866308888_444777705337777p7777cccc53366p669990222666p64446641110555338063305566p666077774433777707p777338p899906644422233cccc446668ccc222666p666555_9244480444555p555022330844337773307777666p666p660366644466011111666600p0666p660611111022244332225544481111_66204440442888086660443323022p2p222550866608443307777828444666p660444660206p666p66844_p44339990333882225509996668809337773309996668808443377733111066p66610366604440222p27773302p2266688p809996668877704488777722p2663111066p666_77778870626602233p3366020555666p66403299909443377733088028111_777744337777055566677778022777666066p66603p3325551_777444p4p4480777733p330880777766_8666p666p666p666068822244_9996661102228870666333083320666p66084433022p2p22255076667772224402233084433777331111p1111_222p26604440442888088777077774447777833777p77770668862233777111_4433999022p2p22330444605553328884446608666966044466020333p3390329997777cccccccccccccccccccccccccccccccc444605553328884446603666cc8666p66444p4p448104448092777703338866cccccccccc7777666777p777999ccccc55566688833099966688cccc1'
offset = 9936 # UTF-8 char code offset required to turn 0 (ascii 48) into the first of the UTF-8 dingbats charset

# Split into lines on '_' (long pause)
tokenized = code_string.split('_')


# In[33]:

def decode_from_multitap(str):
    '''
    Convert multitap keypresses into dingbats.
    
    Multitap keypresses are converted into the language characters that they represent, 
    then converted to UTF-8 dingbats using a character code offset.
    The character code offset is applied to shift the resultant character out of the decoding space:
    E.g. multitap '11111' is converted to '1', but if this remained in the results string it may be 
    converted again, because multitap '1' converts to '.'
    
    The following are ignored:
        c = represents backspace
        p = represents a short pause while the multitap times out to allow the next character to be entered
    '''
    result = str.replace('11111', chr(ord('1')+offset))
    result = result.replace('1111', chr(ord('!')+offset))
    result = result.replace('111', chr(ord('?')+offset))
    result = result.replace('11', chr(ord(',')+offset))
    result = result.replace('1', chr(ord('.')+offset))
    result = result.replace('99999', chr(ord('9')+offset))
    result = result.replace('9999', chr(ord('z')+offset))
    result = result.replace('999', chr(ord('y')+offset))
    result = result.replace('99', chr(ord('x')+offset))
    result = result.replace('9', chr(ord('w')+offset))
    result = result.replace('8888', chr(ord('8')+offset))
    result = result.replace('888', chr(ord('v')+offset))
    result = result.replace('88', chr(ord('u')+offset))
    result = result.replace('8', chr(ord('t')+offset))
    result = result.replace('77777', chr(ord('7')+offset))
    result = result.replace('7777', chr(ord('s')+offset))
    result = result.replace('777', chr(ord('r')+offset))
    result = result.replace('77', chr(ord('q')+offset))
    result = result.replace('7', chr(ord('p')+offset))
    result = result.replace('6666', chr(ord('6')+offset))
    result = result.replace('666', chr(ord('o')+offset))
    result = result.replace('66', chr(ord('n')+offset))
    result = result.replace('6', chr(ord('m')+offset))
    result = result.replace('5555', chr(ord('5')+offset))
    result = result.replace('555', chr(ord('l')+offset))
    result = result.replace('55', chr(ord('k')+offset))
    result = result.replace('5', chr(ord('j')+offset))
    result = result.replace('4444', chr(ord('4')+offset))
    result = result.replace('444', chr(ord('i')+offset))
    result = result.replace('44', chr(ord('h')+offset))
    result = result.replace('4', chr(ord('g')+offset))
    result = result.replace('3333', chr(ord('3')+offset))
    result = result.replace('333', chr(ord('f')+offset))
    result = result.replace('33', chr(ord('e')+offset))
    result = result.replace('3', chr(ord('d')+offset))
    result = result.replace('2222', chr(ord('2')+offset))
    result = result.replace('222', chr(ord('c')+offset))
    result = result.replace('22', chr(ord('b')+offset))
    result = result.replace('2', chr(ord('a')+offset))
    result = result.replace('00', chr(ord('0')+offset))
    result = result.replace('0', chr(ord(' ')+offset))
    return result

def decode_from_offset(str):
    '''
    Convert the UTF-8 dingbat encoding back into the correct ASCII characters.
    '''
    # decode everythig that is not a p (short-pause) or a c (backspace) back into alphanumerics from the UTF-8 dingbat encoding
    result = [(char if char == 'c' or char == 'p' else chr(ord(char)-offset)) for char in str]
    # the result is a list of chars rather than a string, so join them together into a string
    return ''.join(result)

def honour_backspaces(str):
    '''
    Repeatedly look for instances of 'any chaacter but c that is followed by c' and replace 
    botht eh leading character and the c with a null string ('').
    c represents a backspace.
    '''
    # Replace any instance of a single character followed by a c with a blank string, 
    # effectively removing the char before the c
    # '[^c]c' = (any single char that is no c or a linebreak) followed by a c
    p = re.compile('[^c]c')
    result = str
    # Until the input string contains no 'c's, keep removing them and the char before them
    while 'c' in result:
        # Use regex to replace (sub) the matching string with an empty string
        result = p.sub('', result)
    return result


# In[73]:

## INELEGANT ITERATIVE (but working) SOLUTION: USED BECAUSE I COULDN'T FIGURE OUT WHY MY REGEX DIDN'T WORK

# decoded = ''

# for line in tokenized:
#     reversed_encoded = decode_from_multitap(line)[::-1].replace('p', '')
#     # print(line)        
#     # print(decode_from_multitap(line))
#     # print(''.join(decode_from_offset(decode_from_multitap(line))))
#     # reverse the string and remove all 'p's (they've done their job already)
#     # print(decode_from_multitap(line)[::-1].replace('p', '')) 
    
#     backspace_count = 0
#     i = 0
#     result_string = ''
    
#     while i < len(reversed_encoded):
#         # keep a count of the backspace chars as they need to be used
#         if reversed_encoded[i] == 'c':
#             # we found a backspace, so increment the backspace_count and go on to the next character
#             backspace_count += 1
#             i += 1
            
#         elif backspace_count > 0:
#             # we've found a non-backspace
#             # there's a backspace to be used, so... 
#             backspace_count -= 1 # decrement the count
#             # Do nothing - Don't send the char to the result string
#             # Go on to the next char
#             i += 1
            
#         else:
#             # this char is not a backspace and the backspace_count <= 0
#             result_string = reversed_encoded[i] + result_string
#             # go to the next char
#             i += 1
    
#     # print(''.join(decode_from_offset(result_string)))
#     # print()
#     # We've exited the while loop with the result_string reversed back into the original order and
#     #  the backspaces accounted for
#     # Add the result string to the full message list: decoded
#     decoded = decoded + ''.join(decode_from_offset(result_string)) + '\n'
    


# In[34]:

## MORE ELEGANT FUNCTIONAL SOLUTION: USING ACCURATE REGEX THIS TIME :)

decoded = ''

for line in tokenized:
    # The below is split for ease of explanation:
    # Turn the keypresses into offset unicode chars to shift them out of the decoding space,
    #  then delete the short-pauses (p)
    line_result = decode_from_multitap(line).replace('p', '')
    # Use the regex function to apply the backspaces (c)
    line_result = honour_backspaces(line_result)
    # Convert back into a string
    decoded = decoded + '\n' + ''.join(decode_from_offset(honour_backspaces(line_result)))


# In[35]:

# All done: Printed for her viewing pleasure
print(decoded)

print('------------------------------')
print('The answers:')
print('    Password: acidface')
print('    COTOTBP: Cup of tea on the back porch')

