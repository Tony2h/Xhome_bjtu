#-*- coding:utf-8 -*-
import re

def is_all_zh(s):
    for c in s:
        if not ('\u4e00' <= c <= '\u9fa5'):
            return False
    return True

with open("playlist_style1.csv") as file:
    for line in file:
        line1=line.split('\n')
        str = line1[0].split(',')
        if is_all_zh(str[0]):
            songname = str[0]+'\n'
            with open("songname.txt",'a') as f: 
                f.write(songname)
        else:
            pass
        # my_re=re.compile(u'[\u4e00-\u9fa5]+')
        # = re.compile(r'[A-Za-z]',re.S)
        # res = re.findall(my_re,str[0])
        #if len(res):
        #   songname = str[0]+'\n'
        #    with open("songname.txt",'a') as f: 
        #        f.write(songname)
        #else:
        #    pass
            
