'''
Created on Jun 23, 2011

@author: dlemel
'''
import re

def add_to_dict1(d, topic, size, val, type='FF'):
    if not type in d:
        d[type] = {}
    if not topic in d[type]:
        d[type][topic] = {}
    if not size in d[type][topic]:
        d[type][topic][size] = {}
    d[type][topic][size] = val
    
def process_1(file, tested_object):
    tested_re = re.compile(tested_object + ' (\d+)(\w+).*with ([\d\.]+)%')
    d = {}
    topic = ''
    first = True
    acc = {'FF':0, 'other':0}
    for line in open(file).readlines():
        if line[:-1].endswith('?'):
            topic = line[:-1]
            first = True 
        if line.startswith('Accuracy'):
            acc[first and 'FF' or 'other'] = \
                round(float(line.split()[-1][:-2]))
            first = False 
        if line.find('is better than') != -1:
            data = tested_re.search(line)
            size = data.group(1)
            type = data.group(2)
            add_to_dict1(d, topic, size, acc['other'], type)
            add_to_dict1(d, topic, size, acc['FF']) 
    
    fd = open('bla.txt','w')
    for type in d:
        fd.write(type+'\n')
        for topic in d[type]:
            fd.write(topic+'\t')
            tups = d[type][topic].items()
            tups.sort(key=lambda x : int(x[0]))
            fd.write('\t'.join([str(x[1]) for x in tups]))
            fd.write('\n')
        fd.write('\n\n')
    fd.close()

    
def process_2(file, tested_object):
    tested_re = re.compile(tested_object + ' (\d+)(\D+)(\d+).*with ([\d\.]+)%')
    d = {}
    topic = ''
    first = True
    acc = {'FF':0, 'other':0}
    for line in open(file).readlines():
        if line[:-1].endswith('?'):
            topic = line[:-1]
            first = True 
        if line.startswith('Accuracy'):
            acc[first and 'FF' or 'other'] = \
                round(float(line.split()[-1][:-2]))
            first = False 
        if line.find('is better than') != -1:
            data = tested_re.search(line)
            type = data.group(2)
            size = data.group(3)
            #add_to_dict1(d, topic, size, acc['other'], type)
            add_to_dict1(d, topic, size, acc['FF']) 
    
    fd = open('bla.txt','w')
    for type in d:
        fd.write(type+'\n')
        for topic in d[type]:
            fd.write(topic+'\t')
            tups = d[type][topic].items()
            tups.sort(key=lambda x : int(x[0]))
            fd.write('\t'.join([str(x[1]) for x in tups]))
            fd.write('\n')
        fd.write('\n\n')
    fd.close()


if __name__ == '__main__':
    process_1('test1.out', 'Bdio')
    