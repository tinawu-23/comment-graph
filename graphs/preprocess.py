import sys
import json
import csv
import numpy as np

'''
with open('./data.json') as handle:
    dictdump = json.loads(handle.read())

print(dictdump)
'''
# Usage:
# python preprocess.py {matrixfile}
 
# creating a dict file of nodes and links
jsondict = {}
listnodes = []
listlinks = []

uniqnodes = []

if len(sys.argv) == 1:
    filename = input("Data matrix file name: ")
else:
    filename = sys.argv[1]

#filename = '.'+ filename

with open(filename, 'r') as f:
    r = csv.reader(f, delimiter=',')
    for row in r:
        if 'PARENT' in row and 'CHILD' in row:
            continue
        if len(row) != 4:
            print(row, len(row))
            print(row[0])
            print(row[1])
            print(row[2])
            print(row[3])
        uniqnodes.append((row[0],row[1]))
        uniqnodes.append((row[2], row[3]))
            
uniqnodes = list(set(uniqnodes))

for node in uniqnodes:
    nodedict = {}
    nodedict['id'] = node[0]
    sentimentScore = float(node[1])
    if sentimentScore > 0:
        nodedict['color'] = "green"
    elif sentimentScore == 0:
        nodedict['color'] = "yellow"
    else:
        nodedict['color'] = "red"

    listnodes.append(nodedict)

jsondict['nodes'] = listnodes

with open(filename, 'r') as f:
    r = csv.reader(f, delimiter=',')
    for row in r:
        if 'PARENT' in row and 'CHILD' in row:
            continue
        linkdict = {}
        try:
            linkdict['source'], linkdict['target'] = row[0], row[2]
        except:
            continue
        listlinks.append(linkdict)

jsondict['links'] = listlinks

#print(jsondict)

with open('graphs/result.json', 'w') as fp:
    json.dump(jsondict, fp)
