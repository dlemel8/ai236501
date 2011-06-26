'''
Created on Jun 23, 2011

@author: dlemel
'''
import re

def add_to_dict1(d, topic, size, val, type='no'):
    if not type in d:
        d[type] = {}
    if not topic in d[type]:
        d[type][topic] = {}
    if not size in d[type][topic]:
        d[type][topic][size] = {}
    d[type][topic][size] = val
    
def process_1(file, tested_object):
    tested_re = re.compile(tested_object + ' (\d+)(\D+)(\d).*with ([\d\.]+)%')
    d = {}
    topic = ''
    first = True
    acc = {'yes':0, 'no':0}
    for line in open(file).readlines():
        if line[:-1].endswith('?'):
            topic = line[:-1]
            first = True 
        if line.startswith('Accuracy'):
            acc[first and 'no' or 'yes'] = \
                round(float(line.split()[-1][:-2]))
            first = False 
        if line.find('is better than') != -1:
            data = tested_re.search(line)
            size = data.group(1)
            #type = data.group(2)
            add_to_dict1(d, topic, size, acc['no'], 'no')
            add_to_dict1(d, topic, size, acc['yes'], 'yes') 
    
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

def add_to_dict2(d, topic, size, val):
    if not topic in d:
        d[topic] = {}
    if not size in d[topic]:
        d[topic][size] = {}
    d[topic][size] = val
  
def process_2(file, tested_object):
    d = {}
    topic = ''
    first = True
    acc = {'full':0, 'other':0}
    for line in open(file).readlines():
        if line[:-1].endswith('?'):
            topic = line[:-1]
            first = True 
        if line.startswith('Accuracy'):
            acc[first and 'full' or 'other'] = \
                round(float(line.split()[-1][:-2]))
            first = False 
        if line.find('is better than')==-1 and line.find(tested_object)!=-1:
            size = float(line.split(tested_object)[1].split('FF')[1][:-1])
        if line.startswith('~~'):
            add_to_dict2(d, topic, 1.0, acc['full'])
            add_to_dict2(d, topic, size, acc['other'])
    
    fd = open('bla.txt','w')
    for topic in d:
        fd.write(topic+'\t')
        tups = d[topic].items()
        tups.sort(key=lambda x : -float(x[0]))
        fd.write('\t'.join([str(x[1]) for x in tups]))
        fd.write('\n')
    fd.write('\n\n')
    fd.close()


if __name__ == '__main__':
    process_1('test8.out', 'Bdio')
    