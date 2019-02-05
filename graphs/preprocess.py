import sys
import json
import csv
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

filename = '.'+ filename

with open(filename, 'r') as f:
    r = csv.reader(f, delimiter=',')
    for row in r:
        if 'PARENT' in row and 'CHILD' in row:
            continue
        for item in row:
            uniqnodes.append(item)
            
uniqnodes = list(set(uniqnodes))
for node in uniqnodes:
    nodedict = {}
    nodedict['id'] = node
    listnodes.append(nodedict)

jsondict['nodes'] = listnodes

with open(filename, 'r') as f:
    r = csv.reader(f, delimiter=',')
    for row in r:
        if 'PARENT' in row and 'CHILD' in row:
            continue
        linkdict = {}
        try:
            linkdict['source'], linkdict['target'] = row[0], row[1]
        except:
            continue
        listlinks.append(linkdict)

jsondict['links'] = listlinks

#print(jsondict)

with open('graphs/result.json', 'w') as fp:
    json.dump(jsondict, fp)
