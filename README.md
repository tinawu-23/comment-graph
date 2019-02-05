# Reddit Comment Network
2018-2019 Social Sensing Lab Research
 
Creates a comment network in a reddit thread and determines the attitude of the comments.  
To run: ```python main.py -url {reddit post url}```  
Output: ```filename``` matrix data file stored in networkmatrix folder  
   
To generate d3 graph: ```python graphs/preprocess.py {filename}``` (or run with no args, provide filename later)  
This generates a ```result.json``` file being processed by graph.html   
Run ```graph.html``` in browser to view graph
