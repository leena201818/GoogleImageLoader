#!encoding=utf-8
import re

cent = 'i have a dream'



def getName(strr, patt='6号线'):
    patt = re.compile(r'' + patt, re.S)
    result = patt.findall(strr)
    return result


str1 = '我不在16号线，我在6号线'
zzr = getName(str1)
for item in zzr:
    print(item)


z = getName('abdIMAd',patt='MA')
for item in z:
    print(item)