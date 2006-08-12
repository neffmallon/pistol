#!/usr/bin/env python

import re

type = re.compile('@(\w+)\{(\w+),')
end = re.compile('\s*}\s*')
tag = re.compile('\s*(\w+)\s*=\s*(.*)\,*')
empty = re.compile('^\s*$')

def paren_sum(line):
    return line.count('{')-line.count('}')

def strip_parens(sss):
    sss = sss.replace('{','')
    sss = sss.replace('}','')
    return sss

def clump_records(fname):
    'put all of the lines in a single bibtex record together'
    records = []
    record = []
    file = open(fname)

    for line in file:
        if type.match(line):
            if record: records.append(record)
            record = [line]
        else:
            if line: record.append(line)
    return records

def clump_record_lines(records):
    'put all of the multilines together'
    newrecords = []
    for record in records:
        newrecord = []
        newrecords.append(newrecord)
        for line in record:
            if type.match(line) or end.match(line) or tag.match(line):
                newrecord.append(line)
            elif empty.match(line):
                pass
            else:
                newrecord[-1] = newrecord[-1] + ' ' + line
    return newrecords

def parse_records(records):
    for record in records:
        for line in record:
            if type.match(line):
                gs = type.match(line).groups()
                print '%s       %s' % (gs[0],gs[1])
            elif end.match(line):
                pass
            elif tag.match(line):
                gs = tag.match(line).groups()
                print '      %s     %s' % (gs[0],strip_parens(gs[1]))
                pass #print tag.match(line).groups()
            else:
                print "*****",line,

def read_bibtex(fname):
    records = clump_records(fname)
    records = clump_record_lines(records)
    records = parse_records(records)

def main(fname):
    read_bibtex(fname)





if __name__ == '__main__': main('/home/rmuller/Documents/tex/reference.bib') 

