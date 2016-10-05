import numpy as np
import h5py

def map_user():
    ud = {}
    qd = {}
    try: 
        fo = open('../invited_info_train_question_sort.txt','r')
    except:
        print("File invited_info_train_question_sort.txt does not exist.")
        return ud,qd
    u =0
    q =0
    for line in fo:
        line = line.strip('\r\n').split('\t')
        try:
            qd[line[0]]
        except:
            qd[line[0]]=q
            q = q+1
        try:
            ud[line[1]]
        except:
            ud[line[1]]=u
            u=u+1
    fo.close()
    return ud,qd
    
def Map_file():
    ud,qd = map_user()
    fo = open('../invited_info_train_question_sort.txt','r')
    fr = open('../map_invited_info.txt','w')
    for line in fo:
        line = line.strip('\r\n').split('\t')
        s = str(qd[line[0]]) + '\t' + str(ud[line[1]]) + '\t' + line[2] + '\n'
        fr.writelines(s)
    fo.close()
    fr.close()
    '''
    fh = h5py.File('../map_function.h5','w')
    fh.create_dataset('map_question',data =qd)
    fh.create_dataset('map_user',data=ud)
    fh.close()
    '''
    fq =open('../map_question.txt','w')
    fu = open('../map_user.txt','w')
    for i in qd:
        s = i + '\t' + str(qd[i]) + '\n'
        fq.writelines(s)
    fq.close()
    for i in ud:
        s = i + '\t' + str(ud[i]) + '\n'
        fu.writelines(s)
    fu.close()
    
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
        print "parm name only except 'q' or 'u'."
        return None
        
if __name__ == '__main__':
    Map_file()
    
    
    
