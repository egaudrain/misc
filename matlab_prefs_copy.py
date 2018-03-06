#!/usr/bin/env python

# Copies color and font settings from one Matlab preference files to another.
# Note: Matlab needs to be restarted after the copy so they take effect.

# Etienne Gaudrain <egaudrain@gmail.com>
# 2018-03-06

import time, shutil, sys

def parse_file(fname):
    f = open(fname, 'rb')
    d = list()
    for l in f:
        l = l.strip()
        r = dict()
        if l.startswith('#'):
            r['type'] = 'comment'
            r['key'] = None
            r['value'] = l.strip('#')
        else:
            k,v = l.split('=', 1)
            r['key'] = k
            r['value'] = v
            if v.startswith('C'):
                r['type'] = 'color'
            elif v.startswith('F'):
                r['type'] = 'font'
            else:
                r['type'] = 'other'
        d.append(r)
    return d

def display(d):
    for r in d:
        if r['type'] == 'comment':
            print r['type']+' - '+r['value']
        else:
            print r['type']+' - '+r['key']+' = '+r['value']

def write_prefs(d, fname):
    f = open(fname, 'wb')
    for r in d:
        if r['type'] == 'comment':
            f.write('#'+r['value']+'\n')
        else:
            f.write(r['key']+'='+r['value']+'\n')
    f.close()

def copy_prefs(A, B):
    # Copy colors of A to B
    Bdict = dict()
    for i,r in enumerate(B):
        if r['key'] is not None:
            Bdict[r['key']] = i

    for r in A:
        if r['type'] in ['color', 'font']:
            if r['key'] in Bdict:
                Bi = Bdict[r['key']]
                B[Bi]['value'] = r['value']
            else:
                B.append(r)

    return B

def copy_prefs_file(fnameA, fnameB):
    A = parse_file(fnameA)
    B = parse_file(fnameB)
    C = copy_prefs(A, B)
    shutil.copy2(fnameB, fnameB+'.'+time.strftime('%Y%m%d-%H%M%S')+'.old')
    write_prefs(C, fnameB)

if __name__=='__main__':
    if len(sys.argv)<3:
        print 'Usage: '+__file__+' fileA.prf fileB.prf\n'
        print 'Copies fileA.prf color preferences towards fileB.prf.'
        print 'fileB.prf will be overwritten, but a backup copy will be made.'
        exit(1)
    fnameA = sys.argv[1]
    fnameB = sys.argv[2]
    copy_prefs_file(fnameA, fnameB)


