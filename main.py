''' Main Program '''

import warnings
def warn(*args, **kwargs):
    pass
warnings.warn = warn
from textblob import TextBlob
import praw
import pprint
import argparse     # allow the application to accept input filenames as arguments
import io           # for reading from files
import random
import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import json

reddit = praw.Reddit(client_id='9XU4PkAvuNpyWw',
                     client_secret='O6q9aXiKHC0cPLhui6WEJiZMWa0',
                     password='zy5858462',
                     user_agent='testscript by /u/fakebot3',
                     username='mangotangodz')


def getSubComments(comment, allComments, replyList, verbose=True):
    allComments.append(comment)
    if not hasattr(comment, "replies"):
        replies = comment.comments()
        if verbose:
            print("fetching (" + str(len(allComments)) + " comments fetched total)")
    else:
        replies = comment.replies

    for child in replies:
        child.parent = comment.author
        if not child.author:
            child.author = '[deleted]' + str(random.randint(1, 1000000000))
    replyList.append(replies)

    for child in replies:
        getSubComments(child, allComments, replyList, verbose=verbose)


def getAll(r, submissionId, verbose=True):
    submission = r.submission(submissionId)
    comments = submission.comments
    comments.replace_more(limit=0)

    commentsList = []
    replyList = []
    for comment in comments:
        getSubComments(comment, commentsList, replyList, verbose=verbose)
    return commentsList, replyList


def store_json(id, myjson):
    #print(id)
    filename = './redditJson/'+id+'.json'
    with open(filename, 'w') as f:
        f.write(json.dumps(myjson))
    return filename


if __name__ == '__main__':  # running the application
    cnter = 0 
    ### SAVE COMMENTS TO JSON ###
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-url')  # image_url
    args = parser.parse_args()

    random.seed(123)
    redditList = []

    url = args.url
    url_split = (url.split('/'))
    redditID = url_split[(len(url_split))-3]
    redditpost = url_split[7]

    res, replyList = getAll(reddit, redditID)

    for i, j in zip(res, replyList):
        body = i.body.encode('ascii', 'ignore')
        if not i.author:
            author_name = '[deleted]'
        else:
            author_name = bytes.decode(
                i.author.name.encode('ascii', 'ignore',))
        if len(j) == 0:
            has_replies = None
        else:
            has_replies = [(author_name, bytes.decode(x.author.name.encode('ascii', 'ignore',))) if x.author
                           else (author_name, '[deleted]') for x in j]
        if not callable(i.parent):
            parent = str(i.parent)
        else:
            parent = None
        utc = i.created_utc
        redditList.append({"body": bytes.decode(body), "author_name": author_name, "utc": utc,
                           "replies": has_replies, "parent": parent, "score": i.score})

    savedfile = store_json(redditpost, redditList)

    ### CREATE GRAPH ###
    G = nx.DiGraph()

    with open(savedfile) as f:
        data = json.load(f)

    postcontent = redditpost.replace('_', ' ')

    # add center node as the content of post
    G.add_node(postcontent)

    # emotion scores of posts
    red_edges = []
    green_edges = []
    yellow_edges = []

    txtfilename = './networkmatrix/'+redditpost+'.csv'
    f = open(txtfilename, "w")
    print(txtfilename)
    f.write("PARENT,CHILD\n")

    for index, reply in enumerate(data):
        curnode = reply['body']
        curnode_sentiment = TextBlob(curnode)
        if curnode_sentiment.sentiment.polarity > 0:
            green_edges.append((postcontent, curnode))
        elif curnode_sentiment.sentiment.polarity < 0:
            red_edges.append((postcontent, curnode))
        else:
            yellow_edges.append((postcontent, curnode))
        G.add_node(curnode)
        if reply['parent']:
            for i in range(index+1):
                if reply['parent'] == data[index-i]['author_name']:
                    G.add_edges_from([(data[index-i]['body'], reply['body'])])
                    cnter += 1
                    #print("{}   PARENT: {}; REPLY: {}".format(cnter,data[index-i]['body'], reply['body']))
                    # create unique post ids to shorten how each post is represented
                    # author name + length of post + first letter + second to last letter
                    parentstr = data[index-i]['author_name'] + str(len(data[index-i]['body'])) + data[index-i]['body'][0] + data[index-i]['body'][-2]
                    childstr = reply['author_name'] + str(len(reply['body'])) + reply['body'][0] + reply['body'][-2]
                    f.write("{},{}\n".format(parentstr,childstr))
                    break
        else:
            G.add_edges_from([(postcontent, curnode)])
            cnter += 1
            #print("{}   PARENT: {}; REPLY: {}".format(cnter,postcontent, curnode))
            parentstr = "ORIGINALPOST"
            childstr = reply['author_name'] + str(len(reply['body'])) + reply['body'][0] + reply['body'][-2]
            f.write("{},{}\n".format(parentstr, childstr))

    f.close()

    edge_labels = dict([((u, v,)) for u, v, d in G.edges(data=True)])

    pos = nx.spring_layout(G)
    node_labels = {node: node for node in G.nodes()}
    
    edge_colors = ['red' if edge in red_edges else 'green' if edge in green_edges else 'yellow' for edge in G.edges()]
    nx.draw(G, pos, node_color='blue', node_size=1000,
            edge_color=edge_colors, edge_cmap=plt.cm.Reds)
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    pylab.show()
