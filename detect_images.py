import os
import json
# f = open("crawlimage/imageURL.txt", "r")
# i = 0
# for url in f:
#     i += 1
#     command = "python .\web_detect.py --u {} --id {}".format(url.strip(), str(i))
#     os.system(command)

for i in range(145):
    num = i + 1
    fname = 'webDetectionJson/'+str(num)+'.json'
    with open(fname) as j:
        data = json.load(j)
    for url in data[0]["pages_with_matching_images"]:
        link = url["url"]
        if 'reddit' in link:
            print(link)
    for url in data[0]["full_matching_images"]:
        link = url["url"]
        if 'reddit' in link:
            print(link)
    for url in data[0]["partial_matching_images"]:
        link = url["url"]
        if 'reddit' in link:
            print(link)
