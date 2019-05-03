# Reddit Comment Network
2018-2019 Social Sensing Lab Research
 
Creates a comment network in a reddit thread and determines the attitude of the comments.  


To run: ```python main.py -url {reddit post url}```  
Output: ```filename``` matrix data file stored in networkmatrix folder  
   
To generate d3 graph: ```python graphs/preprocess.py {filename}``` (or run with no args, provide filename later)  
This generates a ```result.json``` file being processed by graph.html   
Run ```graph.html``` in browser to view graph

IMPORTANT: due to the unique key naming convention of each comment, it is possible that the filename (matrix file) is malformed;
running ```python graphs/preprocess.py {filename}``` should give you the errors. Simply go to the file and fix them by either a) moving stuff to the same line so each line has 4 items or b) search all for ",," and change them to ",". 


To crawl images from http://hoaxes.org, go to crawlimage folder and run ```python crawler.py```
