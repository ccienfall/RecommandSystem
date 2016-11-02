import numpy as np
import h5py

def map_invited_info():
    ud = Map_load('u')
    qd = Map_load('q')
    try: 
        fo = open('../invited_info_train_question_sort.txt','r')
    except:
        print("File invited_info_train_question_sort.txt does not exist.")
    out = open('../invited_info_train_question_sort_map.txt','w')
    for line in fo:
        line = line.strip('\r\n').split('\t')
        try:
            qid = qd[line[0]]
        except:
            qid = -1
            print('a unknown question')
        try:
            uid = ud[line[1]]
        except:
            uid = -1
            print('a unknown user')
        s = str(qid) + '\t' + str(uid) + '\t' + line[2] + '\n'
        out.writelines(s)
    fo.close()
    out.close()
        
def Map_load(name):
    '''
    pamarater:
        name: Loading question if name is equation 'q'; Loading user if else.
        
    '''
    d = {}
    if name=='q':
        try:
            f = open('../map_question.txt','r')
        except:
            raise ValueError("Missing file: map_question.txt, run Map_file to generate it.")
        for i in f:
            i = i.strip('\r\n').split('\t')
            d[i[0]] = int(i[1])
        return d
    elif name=='u':
        try:
            f = open('../map_user.txt','r')
        except:
            raise ValueError("Missing file: map_question.txt, run Map_file to generate it.")
        for i in f:
            i = i.strip('\r\n').split('\t')
            d[i[0]] = int(i[1])
        return d
    else:
        print "parm name only accept 'q' or 'u'."
        return None

def Map_user_info():
    try:
        f = open('../user_info_sort.txt','r')
    except:
        raise ValueError('Missing file user_info_sort.txt')
    
    out = open('../map_user_extend.txt','w')
    i = 0
    ud = {}
    for line in f:
        line = line.strip('\r\n').split('\t')
        if not (line[0] in ud):
            ud[line[0]] = i
            i = i+1
    for u in ud:
        s = u + '\t' + str(ud[u]) + '\n'
        out.writelines(s)
    out.close()
    f.close()
def Map_question_info():
    try:
        f = open('../question_info_sort.txt','r')
    except:
        raise ValueError('Missing file question_info_sort.txt')
    out = open('../map_question_extend.txt','w')
    i=0
    qd = {}
    for line in f:
        line = line.strip('\r\n').split('\t')
        if not(line[0] in qd):
            qd[line[0]] = i
            i = i+1
    for q in qd:
        s = q + '\t' + str(qd[q]) + '\n'
        out.writelines(s)
    out.close()
    f.close()
if __name__ == '__main__':
    Map_question_info()
    Map_user_info()
    map_invited_info()
    
    
    
