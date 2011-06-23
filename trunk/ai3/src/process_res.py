'''
Created on Jun 23, 2011

@author: dlemel
'''
import re

def process_1(file, tested_object):
    tested_re = re.compile(tested_object + ' (\d+)(\w+).*with ([\d\.]+)%')
    d = {}
    topic = ''
    for line in open(file).readlines():
        if line[:-1].endswith('?'):
            topic = line[:-1] 
        if line.find('is better than') != -1:
            sign = line.startswith(tested_object) and 1 or -1
            data = tested_re.search(line)
            size = data.group(1)
            type = data.group(2)
            val = float(data.group(3))
            
            if not topic in d:
                d[topic] = {}
            if not type in d[topic]:
                d[topic][type] = {}
            if not size in d[topic][type]:
                d[topic][type][size] = {}
            d[topic][type][size] = sign * round(val)
    
    fd = open('bla.txt','w')
    for topic in d:
        fd.write(topic+'\n')
        for type in d[topic]:
            fd.write(type+'\t')
            tups = d[topic][type].items()
            tups.sort(key=lambda x : int(x[0]))
            fd.write('\t'.join([str(x[1]) for x in tups]))
            fd.write('\n')
        fd.write('\n\n')
    fd.close()

if __name__ == '__main__':
    process_1('test1.out', 'Bdio')
    