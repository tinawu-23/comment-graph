import json
import csv
'''
with open('./data.json') as handle:
    dictdump = json.loads(handle.read())

print(dictdump)
'''

# creating a dict file of nodes and links
jsondict = {}
listnodes = []
listlinks = []

uniqnodes = []

with open('../networkmatrix/napa_boy_14_arrested_after_threatening_mass.csv', 'r') as f:
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

with open('../networkmatrix/napa_boy_14_arrested_after_threatening_mass.csv', 'r') as f:
    r = csv.reader(f, delimiter=',')
    for row in r:
        if 'PARENT' in row and 'CHILD' in row:
            continue
        linkdict = {}
        linkdict['source'], linkdict['target'] = row[0], row[1]
        listlinks.append(linkdict)

jsondict['links'] = listlinks

print(jsondict)

with open('result.json', 'w') as fp:
    json.dump(jsondict, fp)
