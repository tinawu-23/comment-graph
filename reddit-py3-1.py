import praw
import pprint

import argparse     # allow the application to accept input filenames as arguments
import io           # for reading from files
import random


import json
reddit = praw.Reddit(client_id='9XU4PkAvuNpyWw',
                     client_secret='O6q9aXiKHC0cPLhui6WEJiZMWa0',
                     password='zy5858462',
                     user_agent='testscript by /u/fakebot3',
                     username='mangotangodz')

# def getSubComments(comment, allComments, replyList, verbose=True):
#     allComments.append(comment)
#     if not hasattr(comment, "replies"):
#         replies = comment.comments()
#         if verbose: print("fetching (" + str(len(allComments)) + " comments fetched total)")
#     else:
#         replies = comment.replies
#     replyList.append(replies)
#     for child in replies:
#         getSubComments(child, allComments, replyList, verbose=verbose)

def getSubComments(comment, allComments, replyList, verbose=True):
    allComments.append(comment)
    if not hasattr(comment, "replies"):
        replies = comment.comments()
        if verbose: print("fetching (" + str(len(allComments)) + " comments fetched total)")
    else:
        replies = comment.replies
        
#     assign random name for [deleted] user/comment
    for child in replies:
        child.parent = comment.author
        if not child.author:
            child.author = '[deleted]' + str(random.randint(1,1000000000))
    replyList.append(replies)
    
    for child in replies:
        getSubComments(child, allComments, replyList, verbose=verbose)
   

def getAll(r, submissionId, verbose=True):
    submission = r.submission(submissionId)
    comments = submission.comments
    # get rid of MoreComments (see https://praw.readthedocs.io/en/latest/tutorials/comments.html#the-replace-more-method) 
    comments.replace_more(limit=0)
    
    commentsList = []
    replyList = []
    for comment in comments:
        getSubComments(comment, commentsList, replyList, verbose=verbose)
    return commentsList, replyList

def store_json(id, myjson):
    print(id)
    filename='./redditJson/'+id+'.json'
    with open( filename, 'w') as f:
        f.write(json.dumps(myjson))


if __name__ == '__main__':  # running the application
    # [START run_web]
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--u')  # image_url
    parser.add_argument('--id')                 # image_id
    args = parser.parse_args()                  # parse the passed-in argument that specifies the URL of the Web image

    random.seed(123)
    # https://www.reddit.com/r/OldSchoolCool/comments/6ays2z/the_famed_19th_century_tornado_that_was_caught_on/
    redditList = []

    url = args.u
    print(url)
    url_split=(url.split('/'))
    redditID=url_split[(len(url_split))-3]
   
    # res = getAll(reddit, redditID) #the id of the reddit post
    res, replyList = getAll(reddit, redditID) 

    for i,j in zip(res, replyList):
        body=i.body.encode('ascii','ignore')
        if not i.author:
            author_name = '[deleted]'
        else:
            author_name= bytes.decode(i.author.name.encode('ascii','ignore',))
        if len(j) == 0:
            has_replies = None
        else:
            has_replies = [(author_name, bytes.decode(x.author.name.encode('ascii','ignore',))) if x.author 
                           else (author_name,'[deleted]') for x in j]
        if not callable(i.parent):
            parent = str(i.parent)
        else:
            parent = None
        utc=i.created_utc
        redditList.append({"body":bytes.decode(body), "author_name":author_name, "utc":utc, 
            "replies": has_replies, "parent": parent, "score": i.score})
      
    store_json(args.id, redditList)

    #pprint.pprint(vars(i)) #this shows all attributes of a comment
    #https://www.reddit.com/r/oddlysatisfying/comments/8wandx/a_perfectly_flat_floor_designed_to_stop_children/
